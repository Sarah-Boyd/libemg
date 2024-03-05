import dearpygui.dearpygui as dpg
from libemg._gui._data_collection_panel import DataCollectionPanel
from libemg._gui._data_import_panel import DataImportPanel
from libemg._gui._visualize_live_signal_panel import VisualizeLiveSignalPanel
import inspect
import time

class GUI:
    def __init__(self, 
                 width=1920,
                 height=1080,
                 args = {},
                 debug=False,
                 video_player_width = 720,
                 video_player_height = 480):
        
        self.args = args
        self.video_player_width = video_player_width
        self.video_player_height = video_player_height
        self.install_global_fields()

        self.window_init(width, height, debug)
        
    def install_global_fields(self):
        # self.global_fields = ['offline_data_handlers', 'online_data_handler']
        self.offline_data_handlers = []   if 'offline_data_handlers' not in self.args.keys() else self.args["offline_data_handlers"]
        self.offline_data_aliases  = []   if 'offline_data_aliases'  not in self.args.keys() else self.args["offline_data_aliases"]
        self.online_data_handler   = None if 'online_data_handler'   not in self.args.keys() else self.args["online_data_handler"]

    def window_init(self, width, height, debug=False):
        dpg.create_context()
        dpg.create_viewport(title="LibEMG",
                            width=width,
                            height=height)
        dpg.setup_dearpygui()
        

        self.file_menu_init()

        dpg.show_viewport()
        dpg.set_exit_callback(self.on_window_close)

        if debug:
            dpg.configure_app(manual_callback_management=True)
            while dpg.is_dearpygui_running():
                jobs = dpg.get_callback_queue()
                dpg.run_callbacks(jobs)
                dpg.render_dearpygui_frame()
        else:
            dpg.start_dearpygui()
        dpg.destroy_context()

    def file_menu_init(self):

        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Exit")
                
            with dpg.menu(label="Data"):
                dpg.add_menu_item(label="Collect Data", callback=self.data_collection_callback)
                dpg.add_menu_item(label="Import Data",  callback=self.import_data_callback )
                dpg.add_menu_item(label="Export Data",  callback=self.export_data_callback)
                dpg.add_menu_item(label="Inspect Data", callback=self.inspect_data_callback)
            
            with dpg.menu(label="Visualize"):
                dpg.add_menu_item(label="Live Signal", callback=self.visualize_livesignal_callback)
            
            with dpg.menu(label="Model"):
                dpg.add_menu_item(label="Train Classifier", callback=self.train_classifier_callback)

            with dpg.menu(label="HCI"):
                dpg.add_menu_item(label="Fitts Law", callback=self.fitts_law_callback)

    def data_collection_callback(self):
        panel_arguments = list(inspect.signature(DataCollectionPanel.__init__).parameters)
        passed_arguments = {i: self.args[i] for i in self.args.keys() if i in panel_arguments}
        self.dcp = DataCollectionPanel(**passed_arguments, gui=self, video_player_width=self.video_player_width, video_player_height=self.video_player_height)
        self.dcp.spawn_configuration_window()

    def import_data_callback(self):
        panel_arguments = list(inspect.signature(DataImportPanel.__init__).parameters)
        passed_arguments = {i: self.args[i] for i in self.args.keys() if i in panel_arguments}
        self.dip = DataImportPanel(**passed_arguments, gui=self)
        self.dip.spawn_configuration_window()

    def export_data_callback(self):
        pass

    def inspect_data_callback(self):
        pass

    def visualize_livesignal_callback(self):
        panel_arguments = list(inspect.signature(VisualizeLiveSignalPanel.__init__).parameters)
        passed_arguments = {i: self.args[i] for i in self.args.keys() if i in panel_arguments}
        self.vlsp = VisualizeLiveSignalPanel(**passed_arguments, gui=self)
        self.vlsp.spawn_configuration_window()

    def train_classifier_callback(self):
        pass

    def fitts_law_callback(self):
        pass

    def on_window_close(self):
        print("Window is closing. Performing clean-up...")
        if 'streamer' in self.args.keys():
            self.args['streamer'].signal.set()
        time.sleep(3)