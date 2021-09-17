import logging
import time
from enum import Enum


class SidecarTerminator:
    class State(Enum):
        NONE_RUNNING = 0
        SIDECAR_RUNNING = 1
        MAIN_RUNNING = 2
        BOTH_RUNNING = 3

    def __init__(self, main_process_name: str, sidecar_process_name: str, lead_time: int = 10, grace_period: int = 10):
        self.main_process_name: str = main_process_name
        self.sidecar_process_name: str = sidecar_process_name
        self.lead_time: int = lead_time
        self.grace_period: int = grace_period
        self.current_state = SidecarTerminator.State.NONE_RUNNING
        self.both_running_state_reached: bool = False
        logging.info(f"Start watching main process '#{self.main_process_name}', "
                     f"sidecar process '#{self.sidecar_process_name}'")

    def watch(self):
        logging.info(f"Starting watch with lead time #{self.lead_time}")
        start_time = time.time()

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > self.grace_period and not self.both_running_state_reached:
                logging.error(f"Processes failed to start in lead time period #{self.lead_time}")
                break
            elif self.both_running_state_reached and self.current_state is SidecarTerminator.State.SIDECAR_RUNNING:
                logging.error(f"Only side car process remaining. Terminating it")

            time.sleep(0.25)

    def main_process_running(self) -> bool:
        pass

    def sidecar_process_running(self) -> bool:
        pass

    def set_current_state(self):
        sc_running:bool = self.sidecar_process_running()
        main_running:bool = self.main_process_running()

        if sc_running and main_running:
            self.current_state = SidecarTerminator.State.BOTH_RUNNING
            self.both_running_state_reached = True
        elif main_running:
            self.current_state = SidecarTerminator.State.MAIN_RUNNING
        elif sc_running:
            self.current_state = SidecarTerminator.State.SIDECAR_RUNNING


if __name__ == '__main__':
    pass

