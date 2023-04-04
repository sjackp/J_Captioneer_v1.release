# J_Captioneer_v1.release

<div align="center">
 <img src="https://tinypic.host/images/2023/04/04/imagfffffasdasde.png" alt="imagfffffasdasde.png" border="0">
<img src="https://tinypic.host/images/2023/04/04/imaasdasdasdgeaaaaaa.png" alt="imaasdasdasdgeaaaaaa.png" border="0">
<img src="https://tinypic.host/images/2023/04/04/imaasdasdasdasfge.png" alt="imaasdasdasdasfge.png" border="0">
<img src="https://tinypic.host/images/2023/04/04/iasdasdsdasdasdmage.png" alt="iasdasdsdasdasdmage.png" border="0">
</div>

# J_Captioneer

J_Captioneer_v1 is a PyQt5-based image browser and caption editor that allows users to view, navigate, and manage images and captions with ease. This streamlines your workflow and makes it easy to edit the captions to your training images. With J_Captioneer_v1, you can quickly and efficiently browse through a directory of images and edit the captions to each one. The app automatically loads all the images and their corresponding text files, and provides a simple and intuitive layout for editing captions. The app also has two find/replace functions as well as a prefix/suffix function.


## Features

J_Captioneer is a PyQt5-based image browser and caption editor that allows users to view, navigate, and manage images and captions with ease. Its features include:

1. Load and display images in a directory.
2. Navigate through images with left and right arrow buttons or keys.
3. Add, edit, and save captions as separate text files associated with each image.
4. Display images as thumbnails for easy navigation.
5. Add prefix and suffix to all captions in a directory.
6. Find and replace text in all captions in a directory.
7. Find specific text and add additional text before or after it in all captions in a directory.
8. Toggle dark mode for a more comfortable viewing experience.

## Installation

### Standalone Executable
Download the standalone executable (`J_Captioneer.exe`) from the [releases](https://github.com/sjackp/J_Captioneer_v1.release/releases) page.

### Installer
Download the installer (`J_Captioneer_Setup.exe`) from the [releases](https://github.com/sjackp/J_Captioneer_v1.release/releases) page and follow the installation steps.

### From Source
Clone the repository and set up the development environment using `requirements.txt`:

git clone https://github.com/sjackp/J_Captioneer_v1.release.git
cd J_Captioneer
pip install -r requirements.txt

To run the application from the source, execute:

python J_Captioneer.py

## Usage

To use J_Captioneer, follow these steps:

1. Launch the application by running `J_Captioneer.exe` (standalone executable) or from the Start Menu (if installed).
2. Click "Choose Directory" to select the folder containing the images you want to work with.
3. Thumbnails of the images will be displayed. Click on a thumbnail to view the image and its associated caption (an empty .txt file will be created if unavailable).
4. Use the left and right arrow buttons or keys to navigate between images.
5. Edit the caption in the text box and click "Save" to save the changes(or Ctrl+s). Captions are saved in the text files with the same name as the image.
6. To return to the thumbnail view, click the "Back" button or press the "Escape" key.
7. Use the menu options under "File" to access additional features such as adding prefix/suffix, find and replace, and toggling dark mode.

## Contributing

If you'd like to contribute to J_Captioneer, please [fork the repository](https://github.com/sjackp/J_Captioneer/fork), create a new branch for your changes, and open a pull request.

## License

J_Captioneer is released under the [MIT License](https://opensource.org/licenses/MIT).
