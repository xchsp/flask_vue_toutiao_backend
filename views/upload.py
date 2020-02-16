import config
from app import app
from flask import jsonify, request
import os
import uuid

from models import Cover


@app.route("/api/upload/", methods=["POST"])
def upload():
    image = request.files.get("file")
    if image:
        if not image.filename.endswith(tuple([".jpg", ".png", ".mp4"])):
            return jsonify({"error": "Image is not valid"}), 409

        # Generate random filename
        filename = str(uuid.uuid4()).replace("-", "") + "." + image.filename.split(".")[-1]

        if not os.path.isdir(config.image_upload_folder):
            os.makedirs(config.image_upload_folder)

        image.save(os.path.join(config.image_upload_folder, filename))
        cover = Cover(
            url=filename,
        ).save()
    else:
        filename = None

    return jsonify(cover.to_public_json())


