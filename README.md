# sort_by_duration

## description

Create a symlink of all videos in subdirectory called `sort_by_duration`.

All symlinks names begin by duration in millisecond and human readable duration. So you can easily sort by duration in your favorite file browser merely sort by name.

For instance `test.mp4` make the symlink `./sort_by_duration/0000013880___(00:00:13:22)___test.mp4`


## Usage

`cd my_path`

`python sort_by_duration.py`

The `-R` switch disable recursion : read only current path, no subdirectory.

## License

[WTFP](LICENSE.txt)
