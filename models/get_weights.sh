FILE=face_mask_detection_checkpoint.pth
if [ ! -f "$FILE" ]; then
    echo "Downloading $FILE ..."
    gdown --id 103pKbKfRHcq7EpEZ_6aBRJWL2b_h9zuR
else
    echo "$FILE Exist!"
    
fi
