
def progress_hook_factory(on_progress, on_done):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                percent = int(downloaded / total * 100)
                on_progress(percent)

        elif d["status"] == "finished":
            on_done(d.get("filename"))

    return hook
