print-course-certificates plugin for Tutor
---------------

Installs the [nau-course-certificate](https://github.com/fccn/nau-course-certificate/) project that allows to print course certificates to PDF on server side.

Requires change the Download Certificate button to be changed to use this application.

Features:
- Generate PDF document server side, so they have consistent presentation
- Digital sign the PDF
- PDF generation cache on S3 Bucket

## Installation

From Git
```bash
pip install git+https://github.com/fccn/tutor-contrib-print-course-certificates@v18.2.5
```

Or from [Pypi](https://pypi.org/project/tutor-contrib-print-course-certificates/)

```bash
pip install tutor-contrib-print-course-certificates==18.2.5
```

## Usage

```bash
tutor plugins enable print-course-certificates
```

## Release

To generate a new release, create a PR/commit with commit message: "chore: preparing release X.X.X", that also changes the `tutorprint_course_certificates/__about__.py` file. Merge it to `main`, then create its Git tag using, `git tag vX.X.X`, then push it `git push --tags`.

## License

This software is licensed under the terms of the AGPLv3.
