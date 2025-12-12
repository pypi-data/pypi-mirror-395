import multiprocessing
import time
import traceback
from queue import Empty

from PySide6.QtCore import QObject, Signal

from qosm.gui.managers import SimulationManager, SimulationAborted, RequestType
from qosm.gui.managers.GBTCSimulationManager import GBTCSimulationManager
from qosm.gui.objects.pipeline import SimulationPipeline


def run_simulation_process(request_data, object_data, source_data, sweep_data, chain, progress_queue, current_file):
    """Function executed in separate process with progress communication"""
    try:
        if chain is None:
            ports_data = [obj for obj in object_data.values() if obj['type'] == 'GBTCPort']
            sample_data = [obj for obj in object_data.values() if obj['type'] == 'GBTCSample']
            request_data = [req for req in request_data.values() if req['type'] == 'GBTC']
            if len(sample_data) == 0:
                raise SimulationAborted('GBTC Sample is missing')
            if len(request_data) == 0:
                raise SimulationAborted('GBTC Request is missing')
            sim_manager = GBTCSimulationManager(request_data[0], ports_data, sample_data[0], sweep_data,
                                                curr_file=current_file)
        else:
            sim_manager = SimulationManager(request_data, object_data, source_data, sweep_data)
            sim_manager.initialise(chain)

        # Create callback to receive progress updates
        def progress_callback(progress_value):
            progress_queue.put(('progress', progress_value))

        # Create callback torsend warning
        def warning_callback(message):
            progress_queue.put(('warning', message))

        # Send initial progress
        progress_queue.put(('progress', 0))

        # Pass callback to simulation manager
        try:
            sim_manager.run(progress_callback=progress_callback, warning_callback=warning_callback)
        except Exception as e:
            traceback.print_exc()
            raise SimulationAborted(str(e))

        # Signal completion with results
        progress_queue.put(('finished', sim_manager.results))

    except SimulationAborted as e:
        progress_queue.put(('error', str(e)))
        return


class SimulationWorker(QObject):
    finished = Signal()
    error = Signal(str, str)
    warning = Signal(str)
    success = Signal(str)
    user_confirm = Signal(object)
    results_ready = Signal(object)
    progress = Signal(str)
    progress_bar = Signal(int)

    def __init__(self, source_data, request_data, object_data, sweep_data, current_file=None):
        super().__init__()
        self.sim_manager = None
        self.source_data = source_data
        self.request_data = request_data
        self.object_data = object_data
        self.sweep_data = sweep_data
        self._should_stop = False
        self.process = None
        self.run_branches = None
        self.current_file = current_file

    def stop(self):
        self._should_stop = True
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join(timeout=5)

    def run(self):
        try:
            types = [item['type'] for item in self.request_data.values()]
            if RequestType.GBTC.name in types:
                # Use GBTC solver, then no branch is needed
                self.run_branches = (None, )
            else:
                # Use Clasic solver
                chains, pipeline = self.run_initialization()
                if len(chains) > 1:
                    self.user_confirm.emit(pipeline)
                    while self.run_branches is None:
                        time.sleep(0.2)
                else:
                    self.run_branches = chains

                if len(self.run_branches) == 0:
                    raise SimulationAborted(f"Invalid pipeline (no valid branch found)")

            self.progress.emit('Starting simulation...')

            if self._should_stop:
                return

            # Create queue for progress communication (BEFORE creating process)
            progress_queue = multiprocessing.Queue()

            # Create and start process
            self.process = multiprocessing.Process(
                target=run_simulation_process,
                args=(self.request_data, self.object_data, self.source_data,
                      self.sweep_data, self.run_branches[0], progress_queue, self.current_file)
            )

            self.process.start()

            # Monitor loop to get progress updates
            simulation_finished = False
            results = None
            attempts = 0

            while not simulation_finished and not self._should_stop:
                # Check for progress messages with timeout
                try:
                    message_type, value = progress_queue.get(timeout=0.1)
                except Empty:  # Queue empty or timeout
                    message_type = value = None

                if message_type == 'progress':
                    # Update progress bar (0-100)
                    self.progress_bar.emit(int(value))
                if message_type == 'warning':
                    self.warning.emit(value)
                elif message_type == 'finished':
                    results = value
                    simulation_finished = True
                elif message_type == 'error':
                    raise SimulationAborted(value)

                # Small pause to avoid CPU overload
                time.sleep(0.0001)

            # Clean up process
            if self.process:
                self.process.join()

            if not self._should_stop and simulation_finished:
                self.success.emit('Simulation completed')
                self.results_ready.emit(results)
            else:
                raise SimulationAborted(f"Simulation process crashed with exit code {self.process.exitcode}")


        except SimulationAborted as e:
            error_msg = str(e)
            error_type = type(e).__name__
            self.error.emit(error_msg, error_type)
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            traceback.print_exc()
            self.error.emit(error_msg, error_type)
        finally:
            if self.process:
                self.process.join()
            self.finished.emit()

    def run_initialization(self):
        # Use local copies
        objects = self.object_data
        active_source = (self.source_data['uuid'], self.source_data['source'])
        objects[active_source[0]] = active_source[1]

        pipeline = SimulationPipeline(objects, active_src_uuid=active_source[0])
        chains_id = pipeline.get_valid_branches(show_id=True)

        return chains_id, pipeline


