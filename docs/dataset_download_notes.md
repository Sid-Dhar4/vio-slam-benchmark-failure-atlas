# Dataset Download Notes

Dataset root used by this project:

```text
~/datasets/euroc
```

Current status:

- The dataset root exists.
- No EuRoC sequence has been downloaded yet.
- The old robotics.ethz.ch individual MH_01_easy ZIP URL timed out from terminal.
- The ETH Research Collection Machine Hall ZIP endpoint connected but returned HTTP 500 from wget.
- A tiny byte-range GET request to the ETH endpoint also returned HTTP 500.

Decision:

- Do not block project development on one failing terminal URL.
- Next attempt should be manual/browser download from the official ETH Research Collection page.
- If official browser download fails, use OpenVINS-listed rosbag mirrors as a temporary path for backend bring-up and document the limitation.

Official sources:

- ASL EuRoC MAV Dataset page: https://projects.asl.ethz.ch/datasets/euroc-mav/
- ETH Research Collection DOI landing page: https://doi.org/10.3929/ethz-b-000690084
- OpenVINS supported datasets page: https://docs.openvins.com/gs-datasets.html
