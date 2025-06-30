import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox # Keep messagebox for now
import threading
import webbrowser
from image_resizer import process_directory, process_image
# from language_manager import LanguageManager # Will be passed in
import os
from tkinterdnd2 import DND_FILES  # 只导入DND_FILES常量，TkinterDnD已在主应用程序中初始化
from drag_drop_handler import handle_file_drop, handle_folder_drop # Add import for handlers

class ImageResizerFrame(ctk.CTkFrame): # Inherit from CTkFrame
    def __init__(self, master, lang_manager): # Accept master and lang_manager
        super().__init__(master)
        self.lang_manager = lang_manager
        self.folder_path = tk.StringVar() # Use tk.StringVar for compatibility or ctk.StringVar
        self.folder_path.trace_add("write", self._on_folder_path_change) # Add trace
        self.resize_mode = tk.StringVar(value="scale") # Default to scale

        # Configure grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        # Add more grid configurations if needed

        # --- Folder Selection --- 
        select_frame = ctk.CTkFrame(self)
        select_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        select_frame.grid_columnconfigure(1, weight=1)

        self.select_label = ctk.CTkLabel(select_frame, text=self.lang_manager.get_text('select_folder')) # Use lang_manager
        self.select_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.folder_entry = ctk.CTkEntry(select_frame, textvariable=self.folder_path)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.select_btn = ctk.CTkButton(select_frame, text=self.lang_manager.get_text('browse'), command=self.select_directory)
        self.select_btn.grid(row=0, column=2, padx=5, pady=5)

        # --- Drag and Drop ---
        try:
            # 注册拖放目标
            self.folder_entry.drop_target_register(DND_FILES)
            # 绑定拖放事件
            self.folder_entry.dnd_bind('<<Drop>>', 
                                      lambda e: handle_folder_drop(e, self.folder_entry, self.lang_manager))
        except Exception as e:
            print(f"文件夹拖拽功能初始化失败: {e}")

        # --- Mode Selection --- 
        self.mode_frame = ctk.CTkFrame(self) # Use CTkFrame
        self.mode_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.mode_frame.grid_columnconfigure(1, weight=1) # Allow input frames to expand

        # self.resize_mode defined earlier

        self.scale_radio = ctk.CTkRadioButton(self.mode_frame, text=self.lang_manager.get_text('scale_mode'), variable=self.resize_mode, value="scale", command=self.toggle_inputs)
        self.scale_radio.grid(row=0, column=0, padx=5, pady=2, sticky='w')

        self.fixed_radio = ctk.CTkRadioButton(self.mode_frame, text=self.lang_manager.get_text('fixed_mode'), variable=self.resize_mode, value="fixed", command=self.toggle_inputs)
        self.fixed_radio.grid(row=1, column=0, padx=5, pady=2, sticky='w')
        
        self.fixed_width_radio = ctk.CTkRadioButton(self.mode_frame, text=self.lang_manager.get_text('fixed_width_mode'), variable=self.resize_mode, value="fixed_width", command=self.toggle_inputs)
        self.fixed_width_radio.grid(row=2, column=0, padx=5, pady=2, sticky='w')
        
        self.fixed_height_radio = ctk.CTkRadioButton(self.mode_frame, text=self.lang_manager.get_text('fixed_height_mode'), variable=self.resize_mode, value="fixed_height", command=self.toggle_inputs)
        self.fixed_height_radio.grid(row=3, column=0, padx=5, pady=2, sticky='w')
        # --- 模式选择结束 ---

        # --- Scale Input --- 
        self.scale_input_frame = ctk.CTkFrame(self.mode_frame)
        self.scale_input_frame.grid(row=0, column=1, padx=5, pady=2, sticky='w')
        self.scale_label = ctk.CTkLabel(self.scale_input_frame, text=self.lang_manager.get_text('scale_label'))
        self.scale_label.pack(side=tk.LEFT)
        self.scale_entry = ctk.CTkEntry(self.scale_input_frame, width=50) # Adjusted width
        self.scale_entry.insert(0, '0.5')
        self.scale_entry.pack(side=tk.LEFT, padx=5)
        # --- 缩放比例结束 ---

        # --- Fixed Resolution Input --- 
        self.fixed_input_frame = ctk.CTkFrame(self.mode_frame)
        self.fixed_input_frame.grid(row=1, column=1, padx=5, pady=2, sticky='w')
        self.width_label = ctk.CTkLabel(self.fixed_input_frame, text=self.lang_manager.get_text('width_label'))
        self.width_label.pack(side=tk.LEFT)
        self.width_entry = ctk.CTkEntry(self.fixed_input_frame, width=60) # Adjusted width
        self.width_entry.pack(side=tk.LEFT, padx=5)
        self.height_label = ctk.CTkLabel(self.fixed_input_frame, text=self.lang_manager.get_text('height_label'))
        self.height_label.pack(side=tk.LEFT)
        self.height_entry = ctk.CTkEntry(self.fixed_input_frame, width=60) # Adjusted width
        self.height_entry.pack(side=tk.LEFT, padx=5)
        # --- 固定分辨率结束 ---
        
        # --- Fixed Width Input --- 
        self.fixed_width_input_frame = ctk.CTkFrame(self.mode_frame)
        self.fixed_width_input_frame.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        self.fixed_width_label = ctk.CTkLabel(self.fixed_width_input_frame, text=self.lang_manager.get_text('width_label'))
        self.fixed_width_label.pack(side=tk.LEFT)
        self.fixed_width_entry = ctk.CTkEntry(self.fixed_width_input_frame, width=60) # Adjusted width
        self.fixed_width_entry.pack(side=tk.LEFT, padx=5)
        # --- 固定宽度结束 ---
        
        # --- Fixed Height Input --- 
        self.fixed_height_input_frame = ctk.CTkFrame(self.mode_frame)
        self.fixed_height_input_frame.grid(row=3, column=1, padx=5, pady=2, sticky='w')
        self.fixed_height_label = ctk.CTkLabel(self.fixed_height_input_frame, text=self.lang_manager.get_text('height_label'))
        self.fixed_height_label.pack(side=tk.LEFT)
        self.fixed_height_entry = ctk.CTkEntry(self.fixed_height_input_frame, width=60) # Adjusted width
        self.fixed_height_entry.pack(side=tk.LEFT, padx=5)
        # --- 固定高度结束 ---

        # --- Process Button --- 
        self.process_btn = ctk.CTkButton(self, text=self.lang_manager.get_text('start_resize'), command=self.start_processing, state=tk.DISABLED)
        self.process_btn.grid(row=2, column=0, padx=10, pady=10)

        # --- Status/Warning Label ---
        self.status_label = ctk.CTkLabel(self, text=self.lang_manager.get_text('status_idle'), text_color='gray') # Initial text
        self.status_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # --- Progress Bar --- 
        self.progress = ctk.CTkProgressBar(self, mode='indeterminate')
        # self.progress will be grid/ungrid as needed





        # GitHub link can be added back if needed, maybe in a help menu or about section in main app
        # For now, removing it from the frame itself

        self.toggle_inputs() # Initialize input states
        self._on_folder_path_change() # Initialize button state based on initial folder_path

    def _on_folder_path_change(self, *args):
        """Callback when folder_path StringVar changes. Updates UI elements accordingly."""
        path = self.folder_path.get()
        if path and os.path.isdir(path):
            self.status_label.configure(text=self.lang_manager.get_text('status_folder_selected').format(folder=os.path.basename(path)), text_color='gray')
            self.process_btn.configure(state=tk.NORMAL)
        else:
            self.process_btn.configure(state=tk.DISABLED)
            if not path: # Path is empty
                self.status_label.configure(text=self.lang_manager.get_text('status_idle'), text_color='gray')
            # else: # Path is not empty but invalid (drag_drop_handler should ideally validate)
            #     self.status_label.configure(text=self.lang_manager.get_text('select_folder_error'), text_color='red')

    def toggle_inputs(self, *args):
        """Enable/disable inputs based on selected mode."""
        mode = self.resize_mode.get()
        # 禁用所有输入框
        self.scale_entry.configure(state=tk.DISABLED)
        self.width_entry.configure(state=tk.DISABLED)
        self.height_entry.configure(state=tk.DISABLED)
        self.fixed_width_entry.configure(state=tk.DISABLED)
        self.fixed_height_entry.configure(state=tk.DISABLED)
        
        # 根据选择的模式启用相应的输入框
        if mode == "scale":
            self.scale_entry.configure(state=tk.NORMAL)
        elif mode == "fixed":
            self.width_entry.configure(state=tk.NORMAL)
            self.height_entry.configure(state=tk.NORMAL)
        elif mode == "fixed_width":
            self.fixed_width_entry.configure(state=tk.NORMAL)
        elif mode == "fixed_height":
            self.fixed_height_entry.configure(state=tk.NORMAL)

    def select_directory(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder) # Triggers _on_folder_path_change via trace

    def start_processing(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror(self.lang_manager.get_text('error_title'), self.lang_manager.get_text('select_folder_error'))
            return

        # Confirmation dialog
        if not messagebox.askyesno(self.lang_manager.get_text('confirm_title'),
                                  self.lang_manager.get_text('confirm_resize_operation').format(folder=os.path.basename(folder))):
            return

        self.select_btn.configure(state=tk.DISABLED)
        self.process_btn.configure(state=tk.DISABLED)
        self.scale_radio.configure(state=tk.DISABLED)
        self.fixed_radio.configure(state=tk.DISABLED)
        self.fixed_width_radio.configure(state=tk.DISABLED)
        self.fixed_height_radio.configure(state=tk.DISABLED)
        self.scale_entry.configure(state=tk.DISABLED)
        self.width_entry.configure(state=tk.DISABLED)
        self.height_entry.configure(state=tk.DISABLED)
        self.fixed_width_entry.configure(state=tk.DISABLED)
        self.fixed_height_entry.configure(state=tk.DISABLED)
        self.progress.grid(row=4, column=0, padx=10, pady=10, sticky="ew") # Use grid
        self.progress.start()
        self.status_label.configure(text=self.lang_manager.get_text('status_processing'), text_color='blue')

        # Use multithreading to avoid freezing the UI
        threading.Thread(target=self.process_images_thread, args=(folder,), daemon=True).start()

    def process_images_thread(self, folder_path): # Pass folder_path
        mode = self.resize_mode.get()
        params = {}
        try:
            if mode == "scale":
                scale = float(self.scale_entry.get())
                if not (0.01 <= scale <= 10.0): # 放宽比例限制
                    raise ValueError("缩放比例需在0.01到10.0之间")
                params['scale'] = scale
            elif mode == "fixed":
                width = int(self.width_entry.get())
                height = int(self.height_entry.get())
                if width <= 0 or height <= 0:
                    raise ValueError("宽度和高度必须是正整数")
                params['width'] = width
                params['height'] = height
            elif mode == "fixed_width":
                width = int(self.fixed_width_entry.get())
                if width <= 0:
                    raise ValueError("宽度必须是正整数")
                params['width'] = width
            elif mode == "fixed_height":
                height = int(self.fixed_height_entry.get())
                if height <= 0:
                    raise ValueError("高度必须是正整数")
                params['height'] = height
            
            # Call the updated process_directory
            process_directory(folder_path, mode=mode, **params) # Use passed folder_path
            # Schedule UI update on the main thread
            self.after(0, self.update_status, self.lang_manager.get_text('status_complete'), 'green')

        except ValueError as ve:
            error_msg = self.lang_manager.get_text('input_error').format(error=str(ve))
            self.after(0, self.update_status, error_msg, 'red')
        except Exception as e:
            error_msg = self.lang_manager.get_text('processing_error').format(error=str(e))
            self.after(0, self.update_status, error_msg, 'red')
        finally:
            # Schedule final UI updates on the main thread
            self.after(0, self.on_processing_complete)

    def update_status(self, message, color):
        """Helper function to update status label text and color."""
        self.status_label.configure(text=message, text_color=color)

    def on_processing_complete(self):
        """Actions to perform on the main thread after processing finishes."""
        self.progress.stop()
        self.progress.grid_forget() # Use grid_forget
        self.select_btn.configure(state=tk.NORMAL)
        self.process_btn.configure(state=tk.NORMAL)
        self.scale_radio.configure(state=tk.NORMAL)
        self.fixed_radio.configure(state=tk.NORMAL)
        self.fixed_width_radio.configure(state=tk.NORMAL)
        self.fixed_height_radio.configure(state=tk.NORMAL)
        self.toggle_inputs() # Restore input states based on mode

    def update_ui_texts(self):
        """Update all UI texts based on the current language."""
        self.select_label.configure(text=self.lang_manager.get_text('select_folder'))
        self.select_btn.configure(text=self.lang_manager.get_text('browse'))
        # Update mode frame text if it were a CTkLabelFrame, but it's a CTkFrame
        self.scale_radio.configure(text=self.lang_manager.get_text('scale_mode'))
        self.fixed_radio.configure(text=self.lang_manager.get_text('fixed_mode'))
        self.fixed_width_radio.configure(text=self.lang_manager.get_text('fixed_width_mode'))
        self.fixed_height_radio.configure(text=self.lang_manager.get_text('fixed_height_mode'))
        self.scale_label.configure(text=self.lang_manager.get_text('scale_label'))
        self.width_label.configure(text=self.lang_manager.get_text('width_label'))
        self.height_label.configure(text=self.lang_manager.get_text('height_label'))
        self.fixed_width_label.configure(text=self.lang_manager.get_text('width_label'))
        self.fixed_height_label.configure(text=self.lang_manager.get_text('height_label'))
        self.process_btn.configure(text=self.lang_manager.get_text('start_process'))
        # Update status label based on current state (this might need more logic)
        # For now, just reset to initial if not processing
        if self.process_btn.cget('state') == tk.NORMAL:
             if not self.folder_path.get():
                 self.status_label.configure(text=self.lang_manager.get_text('status_wait_folder'), text_color='gray')
             else:
                 self.status_label.configure(text=self.lang_manager.get_text('status_folder_selected').format(folder=self.folder_path.get()), text_color='gray')

# Remove standalone execution block
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = ImageResizerApp(root)
#     root.mainloop()
