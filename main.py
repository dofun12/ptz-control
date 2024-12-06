import requests
import sys
import argparse



def generate_template(x, y, xml_path):
    xml = '<s:Envelope ' \
          + 'xmlns:s="http://www.w3.org/2003/05/soap-envelope">' \
          + '\n<s:Body' \
          + '\n    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
          + '\n    xmlns:xsd="http://www.w3.org/2001/XMLSchema">' \
          + '\n    <ContinuousMove xmlns="http://www.onvif.org/ver20/ptz/wsdl">' \
          + '\n        <ProfileToken>' \
          + '\n            stream0_0' \
          + '\n        </ProfileToken>' \
          + '\n        <Velocity>' \
          + '\n           <PanTilt' \
          + f'\n                x="{x}"' \
          + f'\n                y="{y}"' \
          + '\n                xmlns="http://www.onvif.org/ver10/schema"/>' \
          + '\n            </Velocity>' \
          + '\n        </ContinuousMove>' \
          + '\n    </s:Body>' \
          + '\n</s:Envelope>'
    with open(xml_path, 'w') as modified_xml:
        modified_xml.write(xml)
    return xml


def request_move(host: str,xml):
    url = host
    with open(xml) as xml:
        # Give the object representing the XML file to requests.post.
        cam_url = f'http://{url}:8899/onvif/ptz'
        r = requests.post(cam_url, data=xml)




def move(host, position, rate = 0.3):
    xml_path = 'modified.xml'
    generate_template('0', '0', xml_path)
    print(f'Moving camera {position}')
    negative_rate = rate * -1
    positive_rate = rate

    if position == 'up':
        generate_template('0', f'{positive_rate}', xml_path)
    if position == 'down':
        generate_template('0', f'{negative_rate}', xml_path)
    if position == 'left':
        generate_template(f'{negative_rate}', '0', xml_path)
    if position == 'right':
        generate_template(f'{positive_rate}', '0', xml_path)
    request_move(host, xml_path)
    # request_move_str(data)

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('Invalid arguments')
        sys.exit(1)
    parser = argparse.ArgumentParser(description='Move the camera.')
    parser.add_argument('host', type=str, help='The host address of the camera')
    parser.add_argument('direction', metavar='--d', type=str, choices=['up', 'down', 'left', 'right'],
                        help='The direction to move the camera')
    parser.add_argument('rate', type=float, help='The rate of movement')

    args = parser.parse_args()
    move(args.host, args.direction, args.rate)
