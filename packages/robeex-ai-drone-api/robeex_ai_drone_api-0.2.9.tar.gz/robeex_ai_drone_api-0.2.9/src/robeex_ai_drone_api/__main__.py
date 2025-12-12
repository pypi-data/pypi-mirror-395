from robeex_ai_drone_api import RobeexAIDrone
import argparse
from typing import Literal, get_args

Cmd = Literal['land', 'disarm', 'rgb', 'telm']

def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-d", help="disarm", action=argparse.BooleanOptionalAction)
    # parser.add_argument("-l", help="land", action=argparse.BooleanOptionalAction)
    parser.add_argument("-cmd", help="cmd", choices=list(get_args(Cmd)))
    parser.add_argument("-ip", help="drone ip", default="172.168.1.128")
    return parser.parse_args()

def handle_cmd(robeex: RobeexAIDrone, cmd: Cmd):
    match cmd:
        case 'disarm':
            robeex.rc.nav.disarm()
        case 'land':
            robeex.rc.nav.land()
        case 'rgb':
            robeex.rc.rgb.set_full_color(255, 0, 0)
        case 'telm':
            print(robeex.rc.get_next_telemetry_update())

def main():
    args = parse_args()

    robeex = RobeexAIDrone(drone_ip=args.ip)

    cmd: Cmd = args.cmd
    handle_cmd(robeex, cmd)

if __name__ == '__main__':
    main()
