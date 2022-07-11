#!/usr/bin/env python3
import argparse
import csv
import os
import sys
import time
import subprocess
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [FILE] [VOICE] [LANGDIR]",
        description="Generate voice packs from CSV list."
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )

    parser.add_argument('file',
                        type=str,
                        help="CSV Translation file"
                        )

    parser.add_argument('voice',
                        type=str,
                        help="Voice to use"
                        )

    parser.add_argument('langdir',
                        type=str,
                        help="Language subfolder"
                        )

    parser.add_argument('-s',
                        '--delay',
                        type=int,
                        help="Sleep time processing each translation",
                        required=False,
                        default='3'
                        )

    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    csv_file = args.file
    csv_rows = 0
    voice = args.voice
    langdir = args.langdir
    basedir = os.path.dirname(os.path.abspath(__file__))
    outdir = ""
    delay_time = args.delay

    try:
        speech_key = '321ad7266a934042b37bfc835182c9a3'
        service_region = 'eastus'
    except KeyError:
        print("ERROR: Please set the environment variables for Speech and Service Region")
        sys.exit(1)

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region)

    if not(os.path.isfile(csv_file)):
        print("Error: voice file not found")
        sys.exit(1)

    # Get number of rows in CSV file
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        csv_rows = sum(1 for row in reader)

    # Process CSV file
    with open(csv_file, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        line_count = 0
        for row in reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
                csv_rows -= 1
            else:
                if row[4] is None or row[4] == "":
                    outdir = os.path.join(basedir, "SOUNDS", langdir)
                else:
                    outdir = os.path.join(basedir, "SOUNDS", langdir, row[4])
                en_text = row[1]
                text = row[2]
                filename = row[5]
                outfile = os.path.join(outdir, filename)

                if not os.path.exists(outdir):
                    os.makedirs(outdir)

                if text is None or text == "":
                    print(f'[{line_count}/{csv_rows}] Skipping as no text to translate')
                    continue

                if not os.path.isfile(outfile):
                    print(
                        f'[{line_count}/{csv_rows}] Translate "{en_text}" to "{text}", save as "{outdir}/{filename}".')
                    speech_config.speech_synthesis_voice_name = voice
                    audio_config = speechsdk.audio.AudioOutputConfig(
                        filename=outfile)
                    synthesizer = speechsdk.SpeechSynthesizer(
                        speech_config=speech_config, audio_config=audio_config)
                    synthesizer.speak_text_async(text)
                    time.sleep(delay_time)
                else:
                    print(
                        f'[{line_count}/{csv_rows}] Skipping "{filename}" as already exists.')

                line_count += 1

        print(f'Finished processing {csv_rows} entries from "{csv_file}".')


if __name__ == "__main__":
    main()
