import socket


# Default values
DEFAULT_PORT = 8000
DEFAULT_TIMEOUT = 3
DEFAULT_BAUD_RATE = 115200

SYSTEM_COMMAND = 's {}!'
REPORT_COMMAND = 'r {}!'
SOCKET_RECV = 2048
BAUD_RATE_OPTIONS = [115200, 57600, 38400, 19200, 9600, 4800]

INPUT_RANGE = range(0, 5)
OUTPUT_RANGE = range(0, 5)
PRESET_RANGE = range(1, 9)
SCALER_RANGE = range(1, 4)
EDID_RANGE = range(1, 24)
PORT_RANGE = range(1, 65536)


def validate_range(value, label, range):
    assert isinstance(value, int), f'{label} must be integer'
    assert value in range, f'{label} must be in range {range}'


def validate_input(value):
    validate_range(value=value, label='input', range=INPUT_RANGE)


def validate_output(value):
    validate_range(value=value, label='output', range=OUTPUT_RANGE)


def validate_preset(value):
    validate_range(value=value, label='preset', range=PRESET_RANGE)


def validate_scaler(value):
    validate_range(value=value, label='scaler', range=SCALER_RANGE)


def validate_edid(value):
    validate_range(value=value, label='edid_id', range=EDID_RANGE)


def validate_port(value):
    validate_range(value=value, label='port', range=PORT_RANGE)


class HDMI_SCALER:
    BYPASS = 1
    DOWNSCALE = 2
    AUTO = 3


class Blackbird:
    def __init__(self, url, port=DEFAULT_PORT, timeout=DEFAULT_TIMEOUT):
        self.url = url
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.timeout(timeout)

    def connect(self, url=None, port=None):
        url = url or self.url
        port = port or self.port

        assert isinstance(port, int), 'port provided must be integer'
        self.connection.connect((url, port))
        self.connection.recv(SOCKET_RECV)

    def send_command(self, cmd):
        self.connection.send(cmd.encode())
        response = ''

        while True:
            try:
                resp = self.connection.recv(SOCKET_RECV)
                response += resp.decode('utf-8')
            except socket.socket.timeout:
                break

        return response

    def send_report_command(self, cmd):
        return self.send_command(REPORT_COMMAND.format(cmd))

    def send_system_command(self, cmd):
        return self.send_command(SYSTEM_COMMAND.format(cmd))

    def set_power(self, on=True):
        return self.send_system_command(f'power {int(on)}')

    def report_power(self):
        return self.send_report_command('power')

    def reboot(self):
        return self.send_system_command('reboot')

    def model(self):
        return self.send_report_command('type')

    def matrix_status(self):
        return self.send_report_command('status')

    def firmware_version(self):
        return self.send_report_command('fw version')

    def input_connection_status(self, input=0):
        validate_input(input)

        return self.send_report_command(f'link in {input}')

    def output_connection_status(self, output=0):
        validate_input(input)

        return self.send_report_command(f'link out {output}')

    def factory_reset(self):
        return self.send_system_command('reset')

    def set_beep(self, on=True):
        return self.send_system_command(f'beep {int(on)}')

    def set_button_lock(self, on=True):
        return self.send_system_command(f'lock {int(on)}')

    def button_lock_status(self):
        return self.send_report_command('lock')

    def save_preset(self, num):
        validate_preset(num)

        return self.send_system_command(f'save preset {num}')

    def load_preset(self, num):
        validate_preset(num)

        return self.send_system_command(f'recall preset {num}')

    def clear_preset(self, num):
        validate_preset(num)

        return self.send_system_command(f'clear preset {num}')

    def get_preset_details(self, num):
        validate_preset(num)

        return self.send_report_command(f'prefer {num}')

    def get_all_preset_details(self, num):
        response = ''
        for preset_number in PRESET_RANGE:
            response += self.get_preset_details(preset_number)

        return response

    def set_baud_rate(self, rate=DEFAULT_BAUD_RATE):
        return self.send_system_command(f'baud rate {rate}')

    def get_baud_rate(self):
        return self.send_report_command('baud rate')

    def set_control_id(self, id):
        return self.send_system_command(f'id {id}')

    def set_input_to_output(self, input, output=0):
        validate_input(input)
        validate_output(output)

        return self.send_system_command(f'in {input} av out {output}')

    def get_output_signal_status(self, output):
        validate_output(output)

        return self.send_report_command(f'av out {output}')

    def set_output(self, output, on=True):
        validate_output(output)

        return self.send_system_command(f'out {output} stream {int(on)}')

    def get_output_stream_status(self, output):
        validate_output(output)

        return self.send_report_command(f'out {outpuet} stream')

    def set_output_hdmi_scaler(self, output, scaler_mode):
        validate_output(output)
        validate_scaler(scaler_mode)

        return self.send_system_command(f'hdmi {output} scaler {scaler_mode}')

    def get_output_hdmi_scaler(self, output):
        validate_output(output)

        return self.send_report_command(f'hdmi {output} scaler')

    def set_output_hdcp_status(self, output, on=True):
        validate_output(output)

        return self.send_system_command(f'hdmi {output} hdcp {int(on)}')

    def get_output_hdcp_status(self, output):
        validate_output(output)

        return self.send_report_command(f'hdmi {output} hdcp')

    def set_output_arc(self, output, on=True):
        validate_output(output)

        return self.send_system_command(f'hdmi {output} arc {int(on)}')

    def get_output_arc(self, output):
        validate_output(output)

        return self.send_report_command(f'hdmi {output} arc')

    def get_input_edid_status(self, input):
        validate_input(input)

        return self.send_report_command(f'edid in {input}')

    def get_output_hdmi_edid_status(self, output):
        validate_output(output)

        return self.send_report_command(f'edid data hdmi {output}')

    def set_input_edid(self, input, edid_id):
        validate_input(input)
        validate_edid(edid_id)

        return self.send_system_command(f'edid in {input} from {edid_id}')

    def get_ipconfig(self):
        return self.send_report_command('ipconfig')

    def get_mac_addr(self):
        return self.send_report_command('mac addr')

    def set_ip_mode(self, static=False, dhcp=True):
        assert not all([static, dhcp]), 'ip_mode must be static or dhcp'

        if static:
            mode = 0
        elif dhcp:
            mode = 1

        return self.send_system_command(f'ip mode {mode}')

    def get_ip_mode(self):
        return self.send_report_command('ip mode')

    def set_ip_addr(self, ip_addr):
        return self.send_system_command(f'ip addr {ip_addr}')

    def get_ip_addr(self):
        return self.send_report_command('ip addr')

    def set_subnet_mask(self, subnet_mask):
        return self.send_system_command(f'subnet {subnet_mask}')

    def get_subnet_mask(self):
        return self.send_report_command('subnet')

    def set_gateway(self, gateway):
        return self.send_system_command(f'gateway {gateway}')

    def get_gateway(self):
        return self.send_report_command('gateway')

    def set_tcp_port(self, port):
        validate_port(port)

        return self.send_system_command(f'tcp/ip port {port}')

    def get_tcp_port(self):
        return self.send_report_command('tcp/ip port')

    def set_telnet_port(self, port):
        validate_port(port)

        return self.send_system_command(f'telnet port {port}')

    def get_telnet_port(self):
        return self.send_report_command('telnet port')

    def reboot_network(self):
        return self.send_system_command('net reboot')