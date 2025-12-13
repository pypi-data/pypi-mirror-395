import builtins
import logging
import os
import shutil
import sys
import time
import traceback
from contextlib import contextmanager
from functools import partial
from datetime import datetime

original_print = builtins.print
    
class ABFormatter(logging.Formatter):
    file_index = 3
    nu_index = 4
    def __init__(self, log_file, is_format_lib):
        self.log_file = log_file
        self.is_format_lib = is_format_lib
        self.attr_list = ['process', 'asctime', 'levelname', 'pathname', 'lineno', 'funcName']
        init_len = [len(str(os.getpid())), 19, 8, 5, 2, 8]
        self.max_lengths = {key:val for key, val in zip(self.attr_list, init_len)}
        self.just_multiple_lines = False
        super().__init__()
    
    # static method

    @staticmethod
    def logab_custom_print(print_level, *args, **kwargs):
        # Combine arguments into a single message
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '')
        message = sep.join(str(arg) for arg in args) + end
        frame_list = traceback.extract_stack()
        is_custom_print = all(na in frame_list[-2].name for na in ["custom", "print"])
        frame = frame_list[-2] if not is_custom_print else frame_list[-3]
        filename = frame.filename
        funcname = frame.name
        lineno = frame.lineno
        
        # Log the message at the specified print_level
        logging.log(print_level, message, extra={
                'file_id': filename,
                'func_id': funcname,
                'line_id': lineno
            })
    
    @staticmethod
    def format_seconds(seconds):
        if seconds <= 0:
            return "0 seconds"
        units = [
            ("day", 86400),    # 24 * 60 * 60
            ("hour", 3600),    # 60 * 60
            ("minute", 60),
            ("second", 1)
        ]
        result = []
        remaining = float(seconds)
        for unit_name, unit_seconds in units[:-1]:
            if remaining >= unit_seconds:
                value = int(remaining // unit_seconds)
                remaining = remaining % unit_seconds
                result.append(f"{value} {unit_name}{'s' if value > 1 else ''}")
        if remaining > 0 or not result: 
            if remaining.is_integer():
                result.append(f"{int(remaining)} second{'s' if remaining != 1 else ''}")
            else:
                result.append(f"{remaining:.4f} seconds".rstrip('0').rstrip('.'))
        return " ".join(result)


    @staticmethod
    def modify_record_path(record):
        # Get abs and cwd path
        abs_list = record.pathname.split("/")
        cwd_list = os.getcwd().split("/")
        cwd_list[1] = abs_list[1]
        abs_path = os.path.join("/", "/".join(abs_list))
        cwd_path = os.path.join("/", "/".join(cwd_list))

        # Check if path from logab
        if record.module != "log_utils" or hasattr(record, 'func_id'):
            record.pathname = os.path.relpath(abs_path, start=cwd_path)
        else:
            record.pathname =  "logab"
        record.lineno = record.lineno if record.pathname !=  "logab" else 0

        # Print cwd and return
        record.msg = record.msg if record.msg != "logab_print_cwd" else f'Current Working Directory: "{cwd_path}"'
        return record

    # instance method

    def draw_horizontal_line(self):
        placement='+'
        hor_arr = ['-'*(self.max_lengths[item]) for item in self.attr_list]
        hor_arr[self.file_index] = hor_arr[self.file_index] + hor_arr[self.nu_index] + '-'
        hor_arr.pop(self.nu_index)
        hor_arr.append('-'*50)
        hor_line = f'-{placement}-'.join(hor_arr)
        return hor_line
    
    def print_raw(self, content, mode='a', end_char="\n"):
        if self.log_file:
            with open(self.log_file, mode, encoding='utf-8') as file:
                file.write(f"{content}{end_char}")
        else:
            original_print(f"{content}{end_char}", end="", flush=True)

    def rewrite_log(self):
        bak_path = f"{self.log_file}.bak"
        with open (bak_path, mode='w', encoding='utf-8') as file_backup:
            bak_path = file_backup.name
            with open (self.log_file, 'r', encoding='utf-8') as file_log:
                for idx, line in enumerate(file_log):
                    line = line.strip()
                    if line.startswith("----"):
                        hor_line = self.draw_horizontal_line()
                        file_backup.write(f"{hor_line}\n")
                    else:
                        attr_list =line.split("|")
                        newline_arr = []
                        for attr_idx, attr in enumerate(attr_list):
                            if attr_idx > 4:
                                break
                            if attr_idx == self.file_index:
                                lo_li_arr = attr.strip().split(":")
                                new_li = lo_li_arr[0].rjust(self.max_lengths[self.attr_list[self.file_index]])
                                new_lo = lo_li_arr[1].ljust(self.max_lengths[self.attr_list[self.nu_index]])
                                newline_arr.append(f"{new_li}:{new_lo}")
                            else:
                                attr = attr.strip()
                                attr = attr.ljust(self.max_lengths[self.attr_list[attr_idx + (1 if attr_idx > self.file_index else 0)]])
                                newline_arr.append(attr)
                        newline_arr.append("|".join(attr_list[5:]).strip())
                        file_backup.write(f"{' | '.join(newline_arr)}\n")
        try:
            shutil.copyfile(bak_path, self.log_file)
            os.remove(bak_path)
        except Exception as e:
            pass

    def update_max_length(self, record):
        rewrite=False
        for field in self.max_lengths:
            newlen = len(str(getattr(record, field, '')))
            if self.max_lengths[field] < newlen:
                rewrite = True
                self.max_lengths[field] = max(self.max_lengths[field], newlen)
        if rewrite and self.log_file:
            self.rewrite_log()

    def apply_message_format(self, record):
        record.msg = record.getMessage().strip()

        # Define message format
        self._style._fmt = (
            f'%(process){self.max_lengths["process"]}d | '
            f'%(asctime){self.max_lengths["asctime"]}s | '
            f'%(levelname)-{self.max_lengths["levelname"]}s | '
            f'%(pathname){self.max_lengths["pathname"]}s:%(lineno)-{self.max_lengths["lineno"]}d | '
            f'%(funcName)-{self.max_lengths["funcName"]}s | '
            f'%(message)s'
        )

        # Handle multi-line message
        old_msg_list = record.getMessage().split("\n")
        new_msg_list = []
        result_msg = ""
        upper_line = f"{self.draw_horizontal_line()}\n" if (len(old_msg_list) > 1 and self.just_multiple_lines == False) else ""
        lower_line = f"\n{self.draw_horizontal_line()}" if len(old_msg_list) > 1 else ""
        for msg in old_msg_list:
            record.msg = msg
            new_msg_list.append(super().format(record))
        msg_rows = "\n".join(new_msg_list)
        self.just_multiple_lines = True if len(old_msg_list) > 1 else False
        result_msg = f"{upper_line}{msg_rows}{lower_line}"
        return result_msg

    # override method
    
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            return ct.strftime(datefmt)
        return ct.strftime("%Y-%m-%d %H:%M:%S")
    
    def format(self, record):
        # Forward logab to original location
        if hasattr(record, 'func_id'):
            record.pathname = record.file_id
            record.funcName = record.func_id
            record.lineno = record.line_id
        
        # Modify record's path
        record = self.modify_record_path(record)

        # Update max_length and apply format
        is_user_log = "python3" not in record.pathname and "site-packages" not in record.pathname
        if is_user_log or self.is_format_lib:
            if is_user_log:
                self.update_max_length(record)
            result_msg = self.apply_message_format(record)
            return result_msg
        else:
            return record.getMessage()

@contextmanager
def log_wrap(log_file=None, log_level="info", print_level="info", is_format_lib=False):
    # Set up log configuration
    log_level=getattr(logging, log_level.upper(), logging.info)
    handler = logging.StreamHandler() if log_file == None else logging.FileHandler(log_file, mode='a', encoding='utf-8')
    formatter = ABFormatter(log_file=log_file, is_format_lib=is_format_lib)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Set up print configuration
    print_level=getattr(logging, print_level.upper(), logging.info)
    builtins.print = partial(ABFormatter.logab_custom_print, print_level)

    # Print table header
    header_list = [
        ('PID', formatter.max_lengths['process']), 
        ('Time', formatter.max_lengths['asctime']), 
        ('Level', formatter.max_lengths['levelname']), 
        ('File:Nu', formatter.max_lengths['pathname'] + formatter.max_lengths['lineno'] + 1), 
        ('Function', formatter.max_lengths['funcName']), 
        ('Message', 0)
    ]
    header_list_pad = []
    for idx, header_item in enumerate(header_list):
        pad_header = header_item[0].ljust(header_item[1]) if idx != formatter.file_index else header_item[0].rjust(header_item[1])  
        header_list_pad.append(pad_header)
    header_str = f"{' | '.join(header_list_pad)}\n{formatter.draw_horizontal_line()}"
    formatter.print_raw(header_str, mode='w')

    # Print current working directory
    root_logger.critical("logab_print_cwd")
    
    # yield

    # legacy code
    # Print in debug mode (no calculating execution time)
    if 'debugpy' in sys.modules:
        yield
    # Print in normal mode (calculating execution time)
    else:
        start_time = time.time()
        try:
            yield
        except Exception as e:
            # Catch and write error message
            root_logger.error(e)
            hor_line = formatter.draw_horizontal_line()
            tb = traceback.format_exc()
            formatter.print_raw(hor_line)
            formatter.print_raw(tb, end_char="")
            exit()
        finally:
            # Write execution time
            end_time = time.time()
            hor_line = formatter.draw_horizontal_line()
            formatter.print_raw(hor_line)
            root_logger.info(f"Execution time {ABFormatter.format_seconds(end_time-start_time)}")

def log_init():
    logger = logging.getLogger(__name__)
    return logger