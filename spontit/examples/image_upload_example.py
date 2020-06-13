from spontit.resource import SpontitResource
import os


class ImageUploadExample(SpontitResource):

    def dirty_channel_profile_image_upload(self, image_path, is_png, channel_name=None):
        """
        This function explicitly constructs the bytes sent to the server in order to upload a channel profile image.

        The explicit construction of the multi-part request should make it somewhat easier to develop such a request
         in another language.

        :param image_path: the path to the image
        :param is_png: whether or not the image is PNG or JPEG
        :param channel_name: the channel name of the channel whose profile image is being changed. if None, the user
        account's profile image will change
        :return: the response from the request
        """

        # Get the image bytes
        image_data = open(image_path, 'rb')
        image_bytes = image_data.read()

        # Define the boundary value
        boundary_value = b'c5eb4fe57fa3fa84c9695959117aaad4'

        # Initialize the byte array that we will send as data
        final_bytes = bytearray(b'--')

        # Add the channel name to the data, if it is provided
        if channel_name is not None:
            final_bytes.extend(boundary_value)
            final_bytes.extend(b'\r\nContent-Disposition: form-data; name="channelName"\r\n\r\n')
            final_bytes.extend(channel_name.encode())
            final_bytes.extend(b'\r\n--')

        # Add the image data to the data
        final_bytes.extend(boundary_value)
        final_bytes.extend(b'\r\nContent-Disposition: form-data; name="image"; filename="my_file_name"'
                           b'\r\nContent-Type: ')
        if is_png:
            final_bytes.extend(b'image/png')
        else:
            final_bytes.extend(b'image/jpeg')
        final_bytes.extend(b'\r\n\r\n')

        final_bytes.extend(image_bytes)

        # Add the final boundary
        final_bytes.extend(b'\r\n')
        final_bytes.extend(b'--')
        final_bytes.extend(boundary_value)
        final_bytes.extend(b'--')
        final_bytes.extend(b'\r\n')

        # Define the headers.
        headers = self._get_headers()
        headers['Content-Type'] = f'multipart/form-data; multipart/form-data; boundary={boundary_value.decode()}'

        # Send the request
        return self._request(
            payload=final_bytes,
            endpoint="channel/profile_image",
            request_method=self.RequestMethod.POST,
            headers=headers
        )


if __name__ == "__main__":

    img_upload_resource = ImageUploadExample(
        "my_user_id",
        "my_secret_key"
    )

    cwd = os.getcwd()  # Get the current working directory (cwd)
    print(cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print(files)  # Make sure orange.png is in the listed files.

    result = img_upload_resource.dirty_channel_profile_image_upload(
        image_path="orange.png",
        is_png=True
    )
    print(result)

    new_channel_name = "New Channel"
    img_upload_resource.create_channel(new_channel_name)
    result = img_upload_resource.dirty_channel_profile_image_upload(
        image_path="orange.png",
        is_png=True,
        channel_name=new_channel_name
    )
    print(result)
