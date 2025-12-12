import logging
import threading
from datetime import datetime, timezone
from typing import Callable

from licensespring.licensefile.error import ErrorType, WatchdogException

MIN_WATCHDOG_TIMEOUT = 1  # Minimum timeout in minutes
DEFAULT_TIMEOUT_NF = 60  # Default timeout for non-floating licenses in minutes
TIMEOUT_ADJUSTMENT = 15  # Timeout adjustment for floating licenses in seconds


class LicenseWatchdog:
    """
    Monitors and ensures the validity of a software license in a background thread. This watchdog
    can automatically adjust its checking interval based on the type of license (floating or non-floating)
    and supports immediate or delayed license checking after being started. It also allows running
    the monitoring thread as either a daemon or a normal thread.

    Attributes:
        license: The license object being monitored.
        watchdog_callback: A callable function to be called when an exception occurs during license checking.
        timeout: The initial timeout value in minutes for license checking intervals.
        timeout_secs: The calculated timeout in seconds, adjusted for floating licenses if necessary.
        force_exit: A flag indicating whether the watchdog thread should exit its loop and stop.
        predicate: A condition variable predicate used to control the timing of license checks.
        mutex: A threading lock to ensure thread-safe operations.
        cv: A threading condition variable for synchronizing the license checking operations.
        watchdog_thread: The background thread that performs the license checking.

    Methods:
        __init__(self, license, callback: Callable, timeout: int):
            Initializes the LicenseWatchdog with a license object, a callback function, and a timeout value.

        is_active(self):
            Checks if the watchdog's background thread is currently active and running.

        run(self, run_immediately: bool = True, daemon: bool = False):
            Starts the license monitoring process in a background thread. Allows for immediate or delayed start
            of the license checking and sets the thread as a daemon based on the `daemon` argument.

        stop(self):
            Stops the license monitoring process and ensures the background thread is gracefully terminated.

        watchdog_func(self):
            The main function executed by the background thread that periodically checks the license's validity,
            waits for the specified interval or until a stop signal is received, and calls the provided callback function
            in case of exceptions during license checking.
    """

    def __init__(self, license, callback: Callable, timeout: int):
        self.license = license
        self.watchdog_callback = callback
        self.timeout = timeout
        self.timeout_secs = 0
        self.force_exit = False
        self.predicate = False
        self.mutex = threading.Lock()
        self.cv = threading.Condition(self.mutex)
        self.watchdog_thread = None

        need_adjust = False

        if self.timeout <= 0:
            if (
                self.license.licensefile_handler._cache.is_floating
                or self.license.licensefile_handler._cache.is_floating_cloud
            ):
                need_adjust = True
                self.timeout = self.license.licensefile_handler._cache.floating_timeout
                if self.timeout < MIN_WATCHDOG_TIMEOUT:
                    self.timeout = MIN_WATCHDOG_TIMEOUT
            else:
                self.timeout = DEFAULT_TIMEOUT_NF

        self.timeout_secs = self.timeout * 60  # Convert to seconds
        if need_adjust:
            self.timeout_secs -= (
                TIMEOUT_ADJUSTMENT  # Adjust timeout for license check call
            )

    def is_active(self):
        """
        Determines whether the watchdog's background thread is currently active.

        Returns:
            bool: True if the watchdog thread is alive and monitoring the license, False otherwise.
        """

        return self.watchdog_thread and self.watchdog_thread.is_alive()

    def run(self, run_immediately: bool = True, deamon: bool = False):
        """
        Starts the license monitoring process in a separate background thread.

        Args:
            run_immediately: If True, the license check is performed immediately after the thread starts.
                             Otherwise, the first check will occur after the specified timeout period.
            daemon: If True, the background thread is marked as a daemon thread, meaning it will not prevent the
                    program from exiting if it's the only thread left running. If False, the thread is a normal
                    thread that the program will wait for before exiting.

        This method creates and starts a new thread targeting the `watchdog_func` method. It also initializes
        control flags used by the thread for scheduling checks and handling thread termination.
        """

        if self.is_active():
            return

        try:
            self.watchdog_thread = threading.Thread(
                target=self.watchdog_func, daemon=deamon
            )
            self.watchdog_thread.start()
            logging.info("LicenseWatchdog run: thread created")

            with self.mutex:
                self.predicate = run_immediately
                self.force_exit = False

                self.cv.notify_all()

        except Exception as ex:
            logging.info(f"LicenseWatchdog run: exception: {ex}")
            raise Exception(f"Failed to create watchdog thread: {str(ex)}")

    def stop(self):
        """
        Signals the background thread to stop monitoring and exit gracefully.

        This method sets a flag indicating that the thread should stop after completing its current iteration
        of license checking. It then waits for the thread to acknowledge this request and terminate, ensuring
        that all resources are cleanly released.
        """

        if not self.watchdog_thread or not self.watchdog_thread.is_alive():
            return

        with self.mutex:
            self.predicate = True
            self.force_exit = True

            self.cv.notify_all()

        self.watchdog_thread.join()
        self.watchdog_thread = None

    def watchdog_func(self):
        """
        The main function executed by the background thread to perform periodic license checks.

        This function runs in a loop, periodically waiting for a signal to proceed with a license check,
        or for a signal to exit if stopping the watchdog has been requested. It performs the license check
        by calling the `check` method on the monitored license object and handles any exceptions by invoking
        the configured callback function.

        The loop continues until an explicit stop request is received, at which point the thread exits
        cleanly, ensuring all resources are properly released.
        """

        try:
            logging.info("Watchdog started")
            while True:
                with self.cv:
                    self.cv.wait_for(lambda: self.predicate, timeout=self.timeout_secs)
                    self.predicate = False

                if self.force_exit:
                    logging.info(f"break")
                    break

                else:
                    self.license.check()

        except Exception as ex:
            self.watchdog_callback(ex)
        finally:
            logging.info("Watchdog finished")


DEFAULT_TIMEOUT = 60 * 120  # 120 minutes
MIN_TIMEOUT = 60  # 1 minute
API_CALL_SLACK = 15  # Check feature API_CALL_SLACK seconds before it expires
TIMEOUT_SLACK = (
    10  # If feature times out in n seconds, set watchdog timeout to n - TIMEOUT_SLACK
)


class FeatureWatchdog:
    def __init__(self, license, callback, timeout=DEFAULT_TIMEOUT):
        self.license = license
        self.watchdog_callback = callback
        self.timeout = timeout
        self.force_exit = False
        self.predicate = False
        self.feature_codes_and_end_dates = {}
        self.watchdog_thread = None
        self.mutex = threading.Lock()
        self.cv = threading.Condition(self.mutex)

    def __del__(self):
        self.stop()

    def run(self, run_immediately: bool = False, deamon: bool = False):
        """
        Run feature watchdog thread

        Args:
            run_immediately (bool, optional): If True, the license check is performed immediately after the thread starts.
                             Otherwise, the first check will occur after the specified timeout period. Defaults to False.
            deamon (bool, optional): If True, the background thread is marked as a daemon thread, meaning it will not prevent the
                    program from exiting if it's the only thread left running. If False, the thread is a normal
                    thread that the program will wait for before exiting. Defaults to False.

        Raises:
            WatchdogException: Error while Feature WatchDog setup
        """
        try:
            if self.is_active():
                return
            self.watchdog_thread = threading.Thread(
                target=self.watchdog_func, daemon=deamon
            )
            self.watchdog_thread.start()
            logging.info("FeatureWatchdog run: thread created")

            with self.cv:
                self.predicate = run_immediately
                self.force_exit = False
                self.cv.notify_all()

        except Exception as ex:
            logging.error(f"FeatureWatchdog run: exception: {str(ex)}")
            raise WatchdogException(
                ErrorType.FEATURE_WATCHDOG_ERROR,
                f"Failed to create watchdog thread: {str(ex)}",
            )

    def stop(self):
        """
        Signals the background thread to stop monitoring and exit gracefully.
        """
        if not self.watchdog_thread or not self.watchdog_thread.is_alive():
            return

        with self.cv:
            self.predicate = True
            self.force_exit = True
            self.cv.notify_all()

        self.watchdog_thread.join()
        self.watchdog_thread = None

    def add_feature(self, feature: str):
        """
        Add feature inside FeatureWatchdog

        Args:
            feature (str): feature code
        """
        with self.cv:
            feature_obj = self.license.licensefile_handler._cache.get_feature_object(
                feature
            )
            if feature_obj == None:
                return

            if not (
                feature_obj.is_online_floating() or feature_obj.is_offline_floating()
            ):
                return

            if feature_obj.floating_is_expired():
                return

            if feature not in self.feature_codes_and_end_dates:
                logging.info(f"FeatureWatchdog addFeature: {feature}")
                self.feature_codes_and_end_dates[feature] = (
                    feature_obj.floating_end_datetime()
                )
                self.predicate = True
                self.cv.notify_all()

    def remove_feature(self, feature: str):
        """
        Remove feature inside FeatureWatchdog

        Args:
            feature (str): feature code
        """
        with self.cv:
            feature_obj = self.license.licensefile_handler._cache.get_feature_object(
                feature
            )

            if not (
                feature_obj.is_online_floating() or feature_obj.is_offline_floating()
            ):
                return

            if feature in self.feature_codes_and_end_dates:
                logging.info(f"FeatureWatchdog removeFeature: {feature}")
                del self.feature_codes_and_end_dates[feature]

    def watchdog_func(self):
        """
        The main function executed by the background thread to perform periodic feature checks.
        """
        try:
            logging.info("Feature watchdog started")
            while True:
                timeout = self.calculate_timeout()
                with self.cv:
                    self.cv.wait(timeout)
                    if self.force_exit:
                        break
                    self.predicate = False

                for (
                    feature_code,
                    end_datetime,
                ) in self.feature_codes_and_end_dates.items():
                    if self.seconds_remaining(end_datetime) <= API_CALL_SLACK:
                        logging.info(f"feature:{feature_code}, timeout:{end_datetime}")
                        self.license.check_feature(feature_code, False)
                        self.feature_codes_and_end_dates[feature_code] = (
                            self.license.licensefile_handler._cache.get_feature_object(
                                feature_code
                            ).floating_end_datetime()
                        )

        except Exception as ex:
            self.watchdog_callback(ex)
        logging.info("Feature watchdog finished")

    def calculate_timeout(self) -> int:
        """
        Calculates timeout for features check

        Returns:
            int: timeout in seconds
        """
        with self.cv:
            timeout = self.timeout
            for end_datetime in self.feature_codes_and_end_dates.values():
                timeout = min(timeout, self.seconds_remaining(end_datetime))
            if timeout <= TIMEOUT_SLACK:
                return timeout
            return timeout - TIMEOUT_SLACK

    def get_feature_codes(self) -> list:
        with self.cv:
            return list(self.feature_codes_and_end_dates.keys())

    def seconds_remaining(self, end_datetime):
        remaining = (
            end_datetime - datetime.now(timezone.utc).replace(tzinfo=None)
        ).total_seconds()
        return max(0, remaining)

    def is_active(self):
        return self.watchdog_thread and self.watchdog_thread.is_alive()
