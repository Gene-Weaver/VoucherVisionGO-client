# VoucherVisionGO Client

This repository contains only the client component of [VoucherVisionGO](https://github.com/Gene-Weaver/VoucherVisionGO), a tool for automatic label data extraction from museum specimen images.

## About
Last synchronized: Tue Mar  4 20:52:20 UTC 2025

This is a mirror of the `client.py` file from the main VoucherVisionGO repository. It is automatically synchronized when the original file is updated to ensure you always have the latest version.

## Purpose

This repository is designed for users who only need the client component without the full VoucherVisionGO codebase, allowing for:
- Easier integration into existing projects
- Smaller footprint
- Focused functionality
- Simple installation process

## Information 
VoucherVision is designed to transcribe museum specimen labels. Please see the [VoucherVision Github](https://github.com/Gene-Weaver/VoucherVision) for more information. 

As of March 2025, the University of Michigan is allowing free access to VoucherVision. The API is hosted on-demand. It takes about 1 minute for the server to wake up, then subsequent calls are much faster. The API is parallelized and scalable, making this inference much faster than the regular VoucherVision deployment. The tradeoff is that you have less control over the transcription methods. The API supports Google's "gemini-1.5-pro" and "gemini-2.0-flash" for OCR and uses "gemini-2.0-flash" for parsing the unformatted text into JSON. If you want pure speed, use only "gemini-2.0-flash" for both tasks. 

If you want to transcribe different fields, reach out and I can help you develop a prompt or upload your existing prompt to make it available on the API. 

## Requirements

- Python 3.10 or higher
- External dependencies (see installation options below)

## Installation

Choose one of the following installation methods:

### Option 1: Install in your own Python environment from the [PyPi repo](https://pypi.org/project/vouchervision-go-client/)

Install
```bash
pip install vouchervision-go-client
```

Upgrade
```bash
pip install --upgrade vouchervision-go-client

```

### Option 2: Using pip (Install from source locally)

```bash
# Clone
git clone https://github.com/Gene-Weaver/VoucherVisionGO-client.git
cd VoucherVisionGO-client
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Using conda (Install from source locally)
```bash
# Clone
git clone https://github.com/Gene-Weaver/VoucherVisionGO-client.git
cd VoucherVisionGO-client
# Create a virtual environment
conda create -n vvgo-client python=3.10
conda activate vvgo-client

# Install dependencies
pip install -r requirements.txt
```

# Usage Guide (Option 1)

### Programmatic Usage
You can also use the client functions in your own Python code. Install VoucherVisionGO-client from PyPi:

```python
from client import process_vouchers

if __name__ == '__main__':
	process_vouchers(
    server="https://vouchervision-go-XXXXXX.app", 
    output_dir="./output", 
    prompt="SLTPvM_default_chromosome.yaml", 
    image="https://swbiodiversity.org/imglib/seinet/sernec/EKY/31234100396/31234100396116.jpg", 
    directory=None, 
    file_list=None, 
    verbose=True, 
    save_to_csv=True, 
    max_workers=4)

	process_vouchers(
    server="https://vouchervision-go-XXXXXX.app", 
    output_dir="./output2", 
    prompt="SLTPvM_default_chromosome.yaml", 
    image=None, 
    directory="D:/Dropbox/VoucherVisionGO/demo/images", 
    file_list=None, 
    verbose=True, 
    save_to_csv=True, 
    max_workers=4)

```

To get the JSON packet for a single specimen record:

```python
import os
from client import process_image, ordereddict_to_json, get_output_filename

if __name__ == '__main__':
	image_path = "https://swbiodiversity.org/imglib/seinet/sernec/EKY/31234100396/31234100396116.jpg"
	output_dir = "./output"
	output_file = get_output_filename(image_path, output_dir)
	fname = os.path.basename(output_file).split(".")[0]

	result = process_image(fname=fname,
    server_url="https://vouchervision-go-XXXXXX.app", 
    image_path=image_path, 
    output_dir=output_dir, 
    verbose=True, 
    engines= ["gemini-2.0-flash"],
    prompt="SLTPvM_default_chromosome.yaml")
	# Convert to JSON string
	output_str = ordereddict_to_json(result, output_type="json")
	print(output_str)
	# Or keep it as a python dict
	output_dict = ordereddict_to_json(result, output_type="dict")
	print(output_dict)
```

### Viewing prompts from the command line if you install using PyPi
To see an overview of available prompts:
```bash
vv-prompts --server https://vouchervision-go-XXXXXX.app --view 
```

To see the entire chosen prompt:
```bash
vv-prompts --server https://vouchervision-go-XXXXXX.app --prompt "SLTPvM_default.yaml" --raw
```

### Running VoucherVision from the command line if you install using PyPi

Process a single image
```bash
vouchervision --server https://vouchervision-go-XXXXXX.app 
  --image https://swbiodiversity.org/imglib/seinet/sernec/EKY/31234100396/31234100396116.jpg 
  --output-dir ./output 
  --prompt SLTPvM_default_chromosome.yaml 
  --verbose 
  --save-to-csv
```

Process a directory of images
```bash
vouchervision --server https://vouchervision-go-XXXXXX.app 
  --directory ./demo/images 
  --output-dir ./output2 
  --prompt SLTPvM_default_chromosome.yaml 
  --verbose 
  --save-to-csv 
  --max-workers 4
```

Changing OCR engine
```bash
vouchervision --server https://vouchervision-go-XXXXXX.app 
  --image https://swbiodiversity.org/imglib/seinet/sernec/EKY/31234100396/31234100396116.jpg 
  --output-dir ./output3 
  --engines "gemini-2.0-flash"
```

# Usage Guide (Options 2 & 3)
The VoucherVisionGO client provides several ways to process specimen images through the VoucherVision API. Here are the main usage patterns:

### Basic Command Structure
(Don't include the '<' or '>' in the actual commands)
```bash
python client.py --server <SERVER_URL> 
                 --output-dir <OUTPUT_DIR> 
                 --image <SINGLE_IMAGE_PATH_OR_URL> OR --directory <DIRECTORY_PATH> OR --file-list <FILE_LIST_PATH> 
                 --verbose
                 --save-to-csv
                 --engines <ENGINE1> <ENGINE2>
                 --prompt <PROMPT_FILE>
                 --max-workers <NUM_WORKERS>
```

### Required Arguments
The server url:

* `--server`: URL of the VoucherVision API server

One of the following input options:

* `--image`: Path to a single image file or URL
* `--directory`: Path to a directory containing images
* `--file-list`: Path to a file containing a list of image paths or URLs

The path to your local output folder:

* `--output-dir`: Directory to save the output JSON results

### Optional Arguments

* `--engines`: OCR engine options. Recommend not including this and just use the defaults. (default: "gemini-1.5-pro gemini-2.0-flash")
* `--prompt`: Custom prompt file to use. We include a few for you to use. If you created a custom prompt, submit a pull request to add it to [VoucherVisionGO](https://github.com/Gene-Weaver/VoucherVisionGO) or reach out and I can add it for you. (default: "SLTPvM_default.yaml")
* `--verbose`: Print all output to console. Turns off when processing bulk images, only available for single image calls.
* `--save-to-csv`: Save all results to a CSV file in the output directory.
* `--max-workers`: Maximum number of parallel workers. If you are processing 100s/1,000s of images increase this to 8, 16, or 32. Otherwise just skip this and let it use default values. (default: 4, max: 32)

## View Available Prompts

[View the prompts in a web GUI](https://vouchervision-go-XXXXXX.app/prompts-ui)

### List all prompts
First row linux/Mac, second row Windows
```bash
curl "https://vouchervision-go-738307415303.us-central1.run.app/prompts?format=text"
(curl "https://vouchervision-go-738307415303.us-central1.run.app/prompts?format=text").Content
```

### View a specific prompt
```bash
curl "https://vouchervision-go-738307415303.us-central1.run.app/prompts?prompt=SLTPvM_default.yaml&format=text"
(curl "https://vouchervision-go-738307415303.us-central1.run.app/prompts?prompt=SLTPvM_default.yaml&format=text").Content
```

### Getting a specific prompt in JSON format (default)
```bash
curl "https://vouchervision-go-738307415303.us-central1.run.app/prompts?prompt=SLTPvM_default.yaml"
(curl "https://vouchervision-go-738307415303.us-central1.run.app/prompts?prompt=SLTPvM_default.yaml").Content
```


## Example Calls

#### Processing a Single Local Image

```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --image "./demo/images/MICH_16205594_Poaceae_Jouvea_pilosa.jpg" 
  --output-dir "./results/single_image" 
  --verbose
```

#### Processing an Image from URL
```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --image "https://swbiodiversity.org/imglib/h_seinet/seinet/KHD/KHD00041/KHD00041592_lg.jpg" 
  --output-dir "./results/url_image" 
  --verbose
```

#### Processing All Images in a Directory
```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --directory "./demo/images" 
  --output-dir "./results/multiple_images" 
  --max-workers 4
```

#### Processing Images from a CSV List
```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --file-list "./demo/csv/file_list.csv" 
  --output-dir "./results/from_csv" 
  --max-workers 8
```

#### Processing Images from a Text File List
```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --file-list "./demo/txt/file_list.txt" 
  --output-dir "./results/from_txt" 
```

#### Using a Custom Prompt
```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --image "https://swbiodiversity.org/imglib/h_seinet/seinet/KHD/KHD00041/KHD00041592_lg.jpg" 
  --output-dir "./results/custom_prompt" 
  --prompt "SLTPvM_default_chromosome.yaml" 
  --verbose
```

#### Saving Results to CSV
```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --directory "./demo/images" 
  --output-dir "./results/with_csv" 
  --save-to-csv
```

## Output
The client saves the following outputs:

* Individual JSON files for each processed image in the specified output directory.
* A consolidated CSV file with all results if --save-to-csv option is used. First column will be the local filename or filename optained from the url.
* Terminal output with processing details if --verbose option is used. 

## Advanced Usage

#### Using Different OCR Engines

Using BOTH of the best Gemini models for OCR (default)
```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --image "./demo/images/MICH_16205594_Poaceae_Jouvea_pilosa.jpg" 
  --output-dir "./results/custom_engines" 
  --engines "gemini-1.5-pro" "gemini-2.0-flash" 
  --verbose
```

Using only 1 of the best Gemini models for OCR.
```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --image "./demo/images/MICH_16205594_Poaceae_Jouvea_pilosa.jpg" 
  --output-dir "./results/custom_engines" 
  --engines "gemini-2.0-flash" 
  --verbose
```

#### Processing Large Batches with Parallel Workers
For large datasets, you can adjust the number of parallel workers:

```bash
python client.py --server https://vouchervision-go-XXXXXX.app 
  --file-list "./demo/txt/file_list32.txt" 
  --output-dir "./results/parallel" 
  --max-workers 32 
  --save-to-csv
```


## Contributing
If you encounter any issues or have suggestions for improvements, please open an issue in the main repository [VoucherVisionGO](https://github.com/Gene-Weaver/VoucherVisionGO).
