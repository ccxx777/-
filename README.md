# Win11SlideshowPhotos (WPF)

Lightweight Windows 11 slideshow viewer built with C# WPF.

## Run (development)
1. Open a terminal in this folder
2. `dotnet run`

## Publish (single EXE)
1. `dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:IncludeNativeLibrariesForSelfExtract=true`
2. Output: `bin\Release\net8.0-windows\win-x64\publish\Win11SlideshowPhotos.exe`

## Controls
- Mouse wheel: previous/next image
- Ctrl + wheel: zoom
- Left/Right arrows: previous/next image
- Interval: adjust in toolbar (0.05s precision)

## Notes
- If the root folder contains subfolders, the app plays each folder in order.
- If there are no subfolders, it plays images in the root folder.
