from django import forms
from .models_media import MediaItem

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ["title","slug","kind","status","video_url","file","cover_image","description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def clean(self):
        cleaned = super().clean()
        kind = cleaned.get("kind")
        file = cleaned.get("file")
        video_url = cleaned.get("video_url","").strip()

        if kind == "audio":
            if not file:
                raise forms.ValidationError("Audio (MP3) အတွက် File ထည့်ပါ။")
        if kind == "video":
            if not file and not video_url:
                raise forms.ValidationError("Video အတွက် YouTube/Vimeo URL သို့မဟုတ် MP4 file တစ်ခုခုထည့်ပါ။")
        return cleaned
