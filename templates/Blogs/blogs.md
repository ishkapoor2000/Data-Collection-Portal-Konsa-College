Functions used in Blogs

- **cloudinaryUrl**: The URL of the Cloudinary API to upload images.
- **cloudinaryUploadPreset**: The upload preset name to use for uploading images.
- **folder**: The folder name in the Cloudinary account to upload images to.
- **uploadOnCloud**: A function that takes an image file, folder name, image name, Cloudinary URL, and upload preset name, and uploads the image to Cloudinary. Returns the response from the API.
- **editor**: An instance of EditorJS with a custom uploader for the Simple Image Tool.
- **$("#preview-button").click**: A click event handler for the Preview button that saves the editor data, uploads all images to Cloudinary, replaces the original URLs with Cloudinary URLs, shows a preview of the article, sets the form value, and shows the draft button.
- **preview**: A function that takes the editor data, generates a preview of the article, and updates the content of two elements in the DOM.
- **uploadImage**: A function that takes an image file, folder name, and image name, and uploads the image to Cloudinary. Updates the content of two elements in the DOM.
- **$("#header_image_file").on**: A change event handler for the header image file input that uploads the image to Cloudinary and updates the content of two elements in the DOM.

Once the user clicks the "Preview" button, the script first saves the editor data using the editor.save() function. It then filters out all the images from the saved data and uploads them one by one to Cloudinary using the uploadOnCloud() function.

For each image, it retrieves the image URL using a fetch() request, converts the image to a blob, and uploads it to Cloudinary using the uploadOnCloud() function. Once the image is uploaded, it replaces the original URL in the saved data with the Cloudinary URL.

Finally, the script previews the article by iterating over the saved data and rendering each block in HTML. It also sets the form value and shows the draft button.

