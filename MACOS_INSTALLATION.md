# macOS Installation Notes

VidGrab is an open-source project built for learning and community use.
Because Apple requires a **paid developer account** for app notarization,
VidGrab is **not notarized**.

As a result, macOS Gatekeeper may block the app on first launch.
This does **not** mean the app is unsafe.

## ✅ Recommended Way to Open VidGrab on macOS

After downloading and installing:

1. Drag **VidGrab.app** into the **Applications** folder
2. Open **Terminal**
3. Run the following command:

```bash
xattr -dr com.apple.quarantine /Applications/VidGrab.app
```

4. Open **VidGrab** normally from Applications

This only needs to be done **once**.

---

## 🖱️ Alternative (No Terminal)

1. Open **Applications**
2. Right-click **VidGrab.app**
3. Click **Open**
4. When macOS shows a warning, click **Open** again

---

## ❓ Why does macOS show this warning?

Apple requires all distributed apps to be notarized using a paid
Developer ID. Since VidGrab is a free, open-source project,
it is distributed without notarization.

You can always review the full source code here:
👉 **[GitHub Repository](https://github.com/ellaboevans/vidgrab)**

---

## 🔐 Is VidGrab safe?

* VidGrab is fully open source
* No background services
* No system modifications
* No bundled installers

The macOS warning is about **verification**, not malware.

---

## 🛠️ If the app does not open

Run VidGrab directly from Terminal to see error output:

```bash
/Applications/VidGrab.app/Contents/MacOS/VidGrab
```

If you encounter issues, please open an issue on GitHub and include
the output from this command.
