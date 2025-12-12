# Weegit

[![PyPI](https://img.shields.io/pypi/v/weegit?color=blue)](https://pypi.org/project/weegit/)
[![Downloads](https://static.pepy.tech/badge/weegit)](https://pepy.tech/project/weegit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/weegit)](https://pypi.org/project/weegit/)


# Introduction

**Weegit** is a cross-platform application for electrophysiology marking. Works with Windows/Mac/Linux.

It uses specific filesystem architecture that is maintained by the application.
```
$EXPERIMENT_weegit
├── header.json
├── lfp
│   ├── $CH_IDX.lfp
├── sessions
│   ├── $SESSION_NAME.json
```


# Weegit GUI

Run *weegit* through terminal to start GUI.

```bash
$ weegit
```


# Developers
**Weegit** has a convenient interface to work with its data.

### Convert your experiment data to weegit format
```python
from pathlib import Path
from weegit.converter.weegit_io import WeegitIO

PATH_TO_EXP_PARENT_DIR = Path("/path/to/parent/dir/")
EXP_NAME = "20252222"
EXP_DIR = PATH_TO_EXP_PARENT_DIR / EXP_NAME
OUT_WEEGIT_FOLDER = PATH_TO_EXP_PARENT_DIR / (EXP_NAME + "_weegit")
for progress in WeegitIO.convert_from_source_to_weegit(EXP_DIR):
    print(f"\rProgress: {progress}%", end='', flush=True)

print(list(OUT_WEEGIT_FOLDER.glob("*")))
```

***Note: This requires separate $EXPERIMENT folder. Current supported formats are: old Weegit, rhs (XDAQ)***


### Work with the weegit data
```python
from weegit.core.weegit_session import WeegitSessionManager, UserSession

# Init session
session = WeegitSessionManager()
session.init_from_folder(OUT_WEEGIT_FOLDER)

# Work with data
print(session.experiment_data.header)
sweep_idx, start_point, end_point = 0, 0, 10_000
for ch_idx in range(session.experiment_data.header.number_of_channels):
    channel_data = session.experiment_data.data_memmaps[ch_idx][sweep_idx, start_point:end_point]
    print(f"Channel {session.experiment_data.header.channel_info.name[ch_idx]} max voltage val: ",
          max(session.experiment_data.from_int16_to_voltage_val(channel_data, ch_idx)))

# Work with GUI session
session_filename = UserSession.session_name_to_filename("your_session")
session.switch_sessions(session_filename)
print(session.current_user_session.gui_setup)
```


# License

The code and data files in this distribution are licensed under the terms of the GNU General Public License version 3 
as published by the Free Software Foundation. See https://www.gnu.org/licenses/ for a copy of this license.
