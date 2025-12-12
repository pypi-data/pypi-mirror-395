"""
Copyright (c) 2016- 2025, Wiliot Ltd. All rights reserved.

Redistribution and use of the Software in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

  2. Redistributions in binary form, except as used in conjunction with
  Wiliot's Pixel in a product or a Software update for such product, must reproduce
  the above copyright notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the distribution.

  3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
  may be used to endorse or promote products or services derived from this Software,
  without specific prior written permission.

  4. This Software, with or without modification, must only be used in conjunction
  with Wiliot's Pixel or with Wiliot's cloud service.

  5. If any Software is provided in binary form under this license, you must not
  do any of the following:
  (a) modify, adapt, translate, or create a derivative work of the Software; or
  (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
  discover the source code or non-literal aspects (such as the underlying structure,
  sequence, organization, ideas, or algorithms) of the Software.

  6. If you create a derivative work and/or improvement of any Software, you hereby
  irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
  royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
  right and license to reproduce, use, make, have made, import, distribute, sell,
  offer for sale, create derivative works of, modify, translate, publicly perform
  and display, and otherwise commercially exploit such derivative works and improvements
  (as applicable) in conjunction with Wiliot's products and services.

  7. You represent and warrant that you are not a resident of (and will not use the
  Software in) a country that the U.S. government has embargoed for use of the Software,
  nor are you named on the U.S. Treasury Department’s list of Specially Designated
  Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
  You must not transfer, export, re-export, import, re-import or divert the Software
  in violation of any export or re-export control laws and regulations (such as the
  United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
  and use restrictions, all as then in effect

THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
(SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
(A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
(B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
(C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""


import os.path
import os
import pandas as pd
import csv
import datetime
import re
import pathlib
from wiliot_core import InlayTypes,PacketList
try:
    from wiliot_tools.utils.wiliot_gui.wiliot_gui import WiliotGui
except Exception as e:
    print(f'could not import wiliot_gui due to: {e}')
DECRYPTION_MODE = False

try:
    from wiliot_core import DecryptedPacket, DecryptedPacketList
    DECRYPTION_MODE = True
    print('Working on decrypted mode')
except Exception as e:
    pass


alpha_packet_fields = ['common_run_name', 'external_id', 'selected_tag', 'fail_bin_str',
                       'test_start_time', 'trigger_time', 'test_end_time']
MAX_PATH_CHARS = 260


def csv_to_dict(path=None):
    if path:
        with open(path, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            col_names = reader.fieldnames
            data_out = {col: [] for col in col_names}
            try:
                for row in reader:
                    for col in col_names:
                        data_out[col].append(row[col])
            except Exception as e:
                print("couldn't load csv with the following exception: {}".format(e))
        return data_out
    else:
        print('please provide a path')
        return None

def export_decrypted_data(packet_path_in, is_big_file=False, relevant_columns=None, inlay_type=None, ignore_crc=True, packet_version=None, do_decryption=True):
    """

    :param packet_path_in: can be a packet file path or a folder path contains many run folders
                           with packet data at each sub folder
    :type packet_path_in: str
    :param is_big_file: if big data, relevant columns should be specified to shorten the run time
    :type is_big_file: bool
    :param relevant_columns: if big_data is True only the specified columns will be exported
                             according to the decoded data fields
    :type relevant_columns: list or None
    :return: save the decrypted output file with the suffix of _out_<datetime> and
             return a dict where key is the file path and value is dict contains packets_df and statistics_df
    :rtype: dict
    """
    if isinstance(packet_path_in, list):
        file_list = packet_path_in
    elif os.path.isfile(packet_path_in):
        file_list = [packet_path_in]
    elif os.path.isdir(packet_path_in):
        folder_base = pathlib.Path(packet_path_in)
        file_list_path = list(folder_base.rglob("*@packets_data.csv"))
        file_list = [file_in.__str__() for file_in in file_list_path]
        f_list_p2 = list(folder_base.rglob("listener_log_*.log"))
        file_list += [file_in.__str__() for file_in in f_list_p2]
    else:
        raise Exception('packet_path_in is not a file path nor folder : {}'.format(packet_path_in))
    packet_path_out = ''
    de_packet_list = None
    output = {}
    packet_version = float(packet_version) if packet_version is not None else None
    for packet_in in file_list:
        print('process file {}'.format(packet_in))
        timestamp_str = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        if packet_in.endswith('.log'):
            print('analyzing packets...')
            packet_list = PacketList()
            packet_list = packet_list.log_file_to_packet_struct(log_path=packet_in, ignore_crc=ignore_crc)
            if do_decryption:
                de_packet_list = DecryptedPacketList.from_packet_list(packet_list=packet_list, packet_version_by_user=packet_version)
            else:
                de_packet_list = packet_list
            packet_path_out = '{}_out_{}.csv'.format(packet_in.split('.log')[0], timestamp_str)
            stat_path_out = '{}_stat_{}.csv'.format(packet_in.split('.log')[0], timestamp_str)
        elif packet_in.endswith('.csv') or packet_in.endswith('.json'):
            split_str = packet_in.split('.')[-1]
            packet_path_out = '{}_out_{}.csv'.format(packet_in.split(f'.{split_str}')[0], timestamp_str)
            stat_path_out = '{}_stat_{}.csv'.format(packet_in.split(f'.{split_str}')[0], timestamp_str)
            print('analyzing packets...')
            if is_big_file:
                if DECRYPTION_MODE is False:
                    raise Exception('decryption mode is not available, can not run with is_big_file=True')
                else:
                    packet_dict = csv_to_dict(path=packet_in)
                    packet_df = pd.DataFrame(data=packet_dict)
                    decoded_dict = {k: [] for k in relevant_columns}
                    for _, r in packet_df.iterrows():
                        if r['raw_packet'] == '':
                            for k in decoded_dict.keys():
                                decoded_dict[k].append(None)
                        else:
                            p = DecryptedPacket(raw_packet=r['raw_packet'], time_from_start=r['time_from_start'])
                            for k in decoded_dict.keys():
                                decoded_dict[k].append(p.decoded_data[k])

                    for k in decoded_dict.keys():
                        packet_df[k] = decoded_dict[k]
                    packet_df.to_csv(packet_path_out)

            else:
                used_class = DecryptedPacketList if do_decryption else PacketList

                inlay = InlayTypes(inlay_type) if inlay_type else None
                packet_obj = used_class().import_packet_df(
                    path=packet_in,
                    import_all=True,
                    inlay_type=inlay,
                    ignore_crc=ignore_crc,
                )

                de_packet_list = packet_obj
        else:
            print(f'unsupported log file (csv or log) bug got {packet_in}')
            continue

        if not is_big_file:
            de_tag_collection = de_packet_list.to_tag_list()
            de_tag_collection.to_csv(path=get_valid_path_length(packet_path_out),
                                     is_overwrite=True, add_sprinkler_info=True)
            print('save packets data to {}'.format(packet_path_out))

            print('doing tags statistics...')
            stat_df = de_tag_collection.get_statistics()
            stat_df.to_csv(get_valid_path_length(stat_path_out))

            output[packet_path_out] = {'packets_df': de_tag_collection.get_df(), 'statistics_df': stat_df}

    print('done')
    return output


def get_valid_path_length(path_in):
    if len(path_in) >= MAX_PATH_CHARS:
        file_name = os.path.basename(path_in)
        file_name = file_name[(len(path_in) - MAX_PATH_CHARS + 1):]
        path_in = os.path.join(os.path.dirname(path_in), file_name)
    return path_in


def get_files_path():
    inlay_group = tuple(['']+[x.value for x in InlayTypes])

    value_dict = {
        'packets_data_file': {'text': 'Choose packets_data file or listener log file or \nfolder contains packet_data '
                                      'that you want to analyze:',
                              'value': '',
                              'widget_type': "file_input",
                              'options': 'multiple'},
        'inlay': {'text': 'Select inlay',
                  'value': inlay_group},
        'packet_version': {'text': 'Packet Version (relevant for bridge data only)', 'value': ''},
        'bad_crc_en': {'text': 'Filter out bad crc', 'value': False},
    }
    if DECRYPTION_MODE:
        value_dict['pixie_analyzer_en'] = {'text': 'Run PixieAnalyzer', 'value': False}
        value_dict['do_decryption'] = {'text': 'Do Decryption', 'value': True}

    gui = WiliotGui(params_dict=value_dict, title='Analyze packet data')
    gui.run()

    return gui.get_all_values()


if __name__ == '__main__':
    try:
        from wiliot_tools.extended.pixie_analyzer.pixie_analyzer import PixieAnalyzer
    except Exception as e:
        if DECRYPTION_MODE:
            print(e)
        pass
    user_input = get_files_path()
    if user_input is None:
        print('no file was selected. closing the app')
    else:
        p_version = user_input['packet_version'] if user_input['packet_version'] != '' else None
        export_decrypted_data(
                packet_path_in=user_input['packets_data_file'],
                is_big_file=False,
                relevant_columns=None,
                inlay_type=user_input['inlay'],
                ignore_crc=not user_input['bad_crc_en'],
                packet_version=p_version,
                do_decryption=user_input.get('do_decryption', False)
            )
            
        if user_input.get('pixie_analyzer_en', False):
            my_analyzer = PixieAnalyzer()
            [text_log, multi_tag, user_event] = my_analyzer.PacketDecoder().parse(
                input=user_input['packets_data_file'])
            a = my_analyzer.plot_graphs(plot_data=multi_tag, user_event=user_event)
