"""Auto-generated primitives for ilo communication"""

import inspect
from functools import wraps
from typing import get_type_hints


def _typecheck(func):
    hints = get_type_hints(func)
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            if name not in hints:
                continue

            expected = hints[name]

            if not isinstance(value, expected):
                raise TypeError(
                    f"Parameter '{name}' of '{func.__name__}' must be {expected.__name__}, "
                    f"got {type(value).__name__}"
                )

        return func(*args, **kwargs)

    return wrapper



@_typecheck
def safety_stop() -> str:
    """Primitive for safety_stop"""
    return f""

@_typecheck
def handshake_ilo() -> str:
    """Primitive for handshake_ilo"""
    return f"ilo"

@_typecheck
def get_robot_version() -> str:
    """Primitive for get_robot_version"""
    return f"500y"

@_typecheck
def start_firmware_upload(size: int) -> str:
    """Primitive for start_firmware_upload"""
    return f"500x{size}"

@_typecheck
def start_trame_s(trame_s_params: str) -> str:
    """Primitive for start_trame_s"""
    return f"0{trame_s_params}"

@_typecheck
def stop_tasks() -> str:
    """Primitive for stop_tasks"""
    return f"00"

@_typecheck
def get_color_rgb_center() -> str:
    """Primitive for get_color_rgb_center"""
    return f"10c"

@_typecheck
def get_color_rgb_left() -> str:
    """Primitive for get_color_rgb_left"""
    return f"10l"

@_typecheck
def get_color_rgb_right() -> str:
    """Primitive for get_color_rgb_right"""
    return f"10d"

@_typecheck
def get_color_clear() -> str:
    """Primitive for get_color_clear"""
    return f"11"

@_typecheck
def get_line() -> str:
    """Primitive for get_line"""
    return f"12"

@_typecheck
def set_line_threshold_value(threshold: int) -> str:
    """Primitive for set_line_threshold_value"""
    return f"13t{threshold}"

@_typecheck
def get_line_threshold_value() -> str:
    """Primitive for get_line_threshold_value"""
    return f"14"

@_typecheck
def get_accessory_status() -> str:
    """Primitive for get_accessory_status"""
    return f"15"

@_typecheck
def get_sensor_distance() -> str:
    """Primitive for get_sensor_distance"""
    return f"20"

@_typecheck
def get_distance_front() -> str:
    """Primitive for get_distance_front"""
    return f"21"

@_typecheck
def get_distance_right() -> str:
    """Primitive for get_distance_right"""
    return f"22"

@_typecheck
def get_distance_back() -> str:
    """Primitive for get_distance_back"""
    return f"23"

@_typecheck
def get_distance_left() -> str:
    """Primitive for get_distance_left"""
    return f"24"

@_typecheck
def get_imu_info() -> str:
    """Primitive for get_imu_info"""
    return f"30"

@_typecheck
def reset_angle() -> str:
    """Primitive for reset_angle"""
    return f"31"

@_typecheck
def get_raw_imu() -> str:
    """Primitive for get_raw_imu"""
    return f"32"

@_typecheck
def get_battery_info() -> str:
    """Primitive for get_battery_info"""
    return f"40"

@_typecheck
def get_led_color() -> str:
    """Primitive for get_led_color"""
    return f"50"

@_typecheck
def set_led_color_circle(r: str, g: str, b: str) -> str:
    """Primitive for set_led_color_circle"""
    return f"511r{r}g{g}b{b}"

@_typecheck
def set_led_color_circle(r: str, g: str, b: str) -> str:
    """Primitive for set_led_color_circle"""
    return f"512r{r}g{g}b{b}"

@_typecheck
def set_led_shape(shape: str) -> str:
    """Primitive for set_led_shape"""
    return f"52v{shape}"

@_typecheck
def set_led_mode(mode: str, nb_loop: int) -> str:
    """Primitive for set_led_mode"""
    return f"53{mode}/{nb_loop}"

@_typecheck
def set_led_captor(brightness: int) -> str:
    """Primitive for set_led_captor"""
    return f"54l{brightness}"

@_typecheck
def set_led_single(type: str, id: int, red: int, green: int, blue: int) -> str:
    """Primitive for set_led_single"""
    return f"55t{type}d{id}r{red}g{green}b{blue}"

@_typecheck
def display_word(word: str, delay: int, nb_loops: int) -> str:
    """Primitive for display_word"""
    return f"56w{word}d{delay}/{nb_loops}"

@_typecheck
def display_word_slide() -> str:
    """Primitive for display_word_slide"""
    return f"57"

@_typecheck
def set_animation_flag_false() -> str:
    """Primitive for set_animation_flag_false"""
    return f"58"

@_typecheck
def run_command_motor(params: str) -> str:
    """Primitive for run_command_motor"""
    return f"a{params}"

@_typecheck
def ping_motor(ping_status_0: int, ping_status_1: int) -> str:
    """Primitive for ping_motor"""
    return f"60i{ping_status_0}s{ping_status_1}"

@_typecheck
def drive_single_motor_speed(motor_index: int, acc: int, speed: int) -> str:
    """Primitive for drive_single_motor_speed"""
    return f"610i{motor_index}a{acc}v{speed}"

@_typecheck
def get_single_motor_speed(motor_index: int) -> str:
    """Primitive for get_single_motor_speed"""
    return f"611i{motor_index}"

@_typecheck
def drive_single_motor_angle(motor_index: int, acc: int, vel: int, position: int) -> str:
    """Primitive for drive_single_motor_angle"""
    return f"620i{motor_index}a{acc}v{vel}p{position}"

@_typecheck
def get_single_motor_angle(motor_index: int) -> str:
    """Primitive for get_single_motor_angle"""
    return f"621i{motor_index}"

@_typecheck
def get_single_motor_temp(motor_index: int) -> str:
    """Primitive for get_single_motor_temp"""
    return f"63i{motor_index}"

@_typecheck
def get_single_motor_volt(motor_index: int) -> str:
    """Primitive for get_single_motor_volt"""
    return f"64i{motor_index}"

@_typecheck
def get_single_motor_load(motor_index: int) -> str:
    """Primitive for get_single_motor_load"""
    return f"65i{motor_index}"

@_typecheck
def get_single_motor_current(motor_index: int) -> str:
    """Primitive for get_single_motor_current"""
    return f"66i{motor_index}"

@_typecheck
def get_single_motor_move(motor_index: int) -> str:
    """Primitive for get_single_motor_move"""
    return f"67i{motor_index}"

@_typecheck
def set_motors_ilo_acc(acc: int) -> str:
    """Primitive for set_motors_ilo_acc"""
    return f"680a{acc}"

@_typecheck
def get_motors_ilo_acc() -> str:
    """Primitive for get_motors_ilo_acc"""
    return f"681"

@_typecheck
def set_tempo_pos(tempo_pos: int) -> str:
    """Primitive for set_tempo_pos"""
    return f"690t{tempo_pos}"

@_typecheck
def get_tempo_pos() -> str:
    """Primitive for get_tempo_pos"""
    return f"691"

@_typecheck
def set_pid(Kp: int, Ki: int, Kd: int) -> str:
    """Primitive for set_pid"""
    return f"70p{Kp}i{Ki}d{Kd}"

@_typecheck
def get_pid() -> str:
    """Primitive for get_pid"""
    return f"71"

@_typecheck
def check_auto_mode(current_auto_mode: int) -> str:
    """Primitive for check_auto_mode"""
    return f"80{current_auto_mode}"

@_typecheck
def set_wifi_credentials(ssid: str, password: str) -> str:
    """Primitive for set_wifi_credentials"""
    return f"90{ssid}{{|||}}{password}"

@_typecheck
def get_wifi_credentials() -> str:
    """Primitive for get_wifi_credentials"""
    return f"92"

@_typecheck
def get_hostname() -> str:
    """Primitive for get_hostname"""
    return f"93"

@_typecheck
def get_hostname_legacy() -> str:
    """Primitive for get_hostname_legacy"""
    return f"930"

@_typecheck
def set_name(name: str) -> str:
    """Primitive for set_name"""
    return f"94n{name}"

@_typecheck
def set_server_status(status: int) -> str:
    """Primitive for set_server_status"""
    return f"95s{status}"

@_typecheck
def get_server_status() -> str:
    """Primitive for get_server_status"""
    return f"96"

@_typecheck
def get_accessory_data() -> str:
    """Primitive for get_accessory_data"""
    return f"100"

@_typecheck
def get_accessory_info() -> str:
    """Primitive for get_accessory_info"""
    return f"101"

@_typecheck
def very_very_usefull() -> str:
    """Primitive for very_very_usefull"""
    return f"102"

@_typecheck
def set_debug_state(state: int) -> str:
    """Primitive for set_debug_state"""
    return f"103s{state}"

@_typecheck
def start_diag() -> str:
    """Primitive for start_diag"""
    return f"110"

@_typecheck
def get_manufacturing_date() -> str:
    """Primitive for get_manufacturing_date"""
    return f"120"

@_typecheck
def set_manufacturing_date(date: str) -> str:
    """Primitive for set_manufacturing_date"""
    return f"121s{date}"

@_typecheck
def get_first_use_date() -> str:
    """Primitive for get_first_use_date"""
    return f"130"

@_typecheck
def set_first_use_date(date: str) -> str:
    """Primitive for set_first_use_date"""
    return f"131s{date}"

@_typecheck
def get_product_version() -> str:
    """Primitive for get_product_version"""
    return f"140"

@_typecheck
def set_product_version(version: str) -> str:
    """Primitive for set_product_version"""
    return f"141s{version}"

@_typecheck
def get_product_id() -> str:
    """Primitive for get_product_id"""
    return f"150"

@_typecheck
def set_product_id(product_id: str) -> str:
    """Primitive for set_product_id"""
    return f"151s{product_id}"

@_typecheck
def get_review_date() -> str:
    """Primitive for get_review_date"""
    return f"160"

@_typecheck
def set_review_date(date: str) -> str:
    """Primitive for set_review_date"""
    return f"161s{date}"

@_typecheck
def set_auto_setup(auto_setup: int) -> str:
    """Primitive for set_auto_setup"""
    return f"170a{auto_setup}"


__all__ = (
  "safety_stop",
  "handshake_ilo",
  "get_robot_version",
  "start_firmware_upload",
  "start_trame_s",
  "stop_tasks",
  "get_color_rgb_center",
  "get_color_rgb_left",
  "get_color_rgb_right",
  "get_color_clear",
  "get_line",
  "set_line_threshold_value",
  "get_line_threshold_value",
  "get_accessory_status",
  "get_sensor_distance",
  "get_distance_front",
  "get_distance_right",
  "get_distance_back",
  "get_distance_left",
  "get_imu_info",
  "reset_angle",
  "get_raw_imu",
  "get_battery_info",
  "get_led_color",
  "set_led_color_circle",
  "set_led_color_circle",
  "set_led_shape",
  "set_led_mode",
  "set_led_captor",
  "set_led_single",
  "display_word",
  "display_word_slide",
  "set_animation_flag_false",
  "run_command_motor",
  "ping_motor",
  "drive_single_motor_speed",
  "get_single_motor_speed",
  "drive_single_motor_angle",
  "get_single_motor_angle",
  "get_single_motor_temp",
  "get_single_motor_volt",
  "get_single_motor_load",
  "get_single_motor_current",
  "get_single_motor_move",
  "set_motors_ilo_acc",
  "get_motors_ilo_acc",
  "set_tempo_pos",
  "get_tempo_pos",
  "set_pid",
  "get_pid",
  "check_auto_mode",
  "set_wifi_credentials",
  "get_wifi_credentials",
  "get_hostname",
  "get_hostname_legacy",
  "set_name",
  "set_server_status",
  "get_server_status",
  "get_accessory_data",
  "get_accessory_info",
  "very_very_usefull",
  "set_debug_state",
  "start_diag",
  "get_manufacturing_date",
  "set_manufacturing_date",
  "get_first_use_date",
  "set_first_use_date",
  "get_product_version",
  "set_product_version",
  "get_product_id",
  "set_product_id",
  "get_review_date",
  "set_review_date",
  "set_auto_setup",
)