# Failure Atlas

Status: public benchmark release with fair-overlap metrics, event summaries, failure cards, error timelines, CI, and one-command derived-artifact reproduction.

This failure atlas summarizes observed behavior from ORB-SLAM3 and OpenVINS on three EuRoC Machine Hall visual-inertial sequences.

The goal is not only to report accuracy, but to explain where each estimator struggled and what evidence supports that interpretation.

## Important evaluation caveats

- ORB-SLAM3 was run on full EuRoC sequence timestamps.
- OpenVINS was run through its ROS 1 serial EuRoC workflow using Machine Hall start offsets.
- OpenVINS used bag_start=40 seconds for MH_01_easy and bag_start=5 seconds for MH_03_medium and MH_05_difficult.
- Original metrics report each backend on its available output trajectory.
- Fair-overlap metrics crop ground truth, ORB-SLAM3, and OpenVINS to the common timestamp interval for each sequence.
- Runtime numbers should not yet be interpreted as a fair speed comparison because ORB-SLAM3 and OpenVINS were run through different example pipelines.
- All OpenVINS runs saved trajectory and timing files but ended with a ROS shutdown LibraryUnloadException, so they are marked completed_with_shutdown_exception.

## Summary table

See:

- results/metrics.csv
- results/tables/benchmark_summary.md
- results/tables/event_summary.md
- results/tables/fair_overlap_summary.md
- reports/failure_cards/MH_01_easy.md
- reports/failure_cards/MH_03_medium.md
- reports/failure_cards/MH_05_difficult.md
- results/plots/errors/MH_01_easy_error_timeline.png
- results/plots/errors/MH_03_medium_error_timeline.png
- results/plots/errors/MH_05_difficult_error_timeline.png

## Sequence-level observations

### MH_01_easy

MH_01_easy is the sanity-check sequence. Both systems produced trajectories.

Observed metrics:

- ORB-SLAM3 APE SE(3)-aligned RMSE: 0.048717 m
- ORB-SLAM3 RPE translation RMSE: 0.003445 m
- OpenVINS APE SE(3)-aligned RMSE: 0.090810 m
- OpenVINS RPE translation RMSE: 0.002152 m

Observed behavior:

- ORB-SLAM3 reported early IMU/initialization messages including not enough acceleration and not enough motion for initialization, then recovered and saved a trajectory.
- OpenVINS produced an estimate and timing log, but ended with a ROS shutdown LibraryUnloadException.
- OpenVINS used bag_start=40 seconds, so the estimate covers a cropped part of the sequence.

Interpretation:

- ORB-SLAM3 achieved lower aligned APE on this sequence, while OpenVINS had slightly lower frame-to-frame translational RPE.
- This suggests ORB-SLAM3 produced a better globally aligned trajectory on this run, while OpenVINS local incremental motion was still smooth.
- The comparison should be treated carefully because of OpenVINS start offset and shutdown exception.

### MH_03_medium

MH_03_medium is the moderate-difficulty sequence.

Observed metrics:

- ORB-SLAM3 APE SE(3)-aligned RMSE: 0.034222 m
- ORB-SLAM3 RPE translation RMSE: 0.004600 m
- OpenVINS APE SE(3)-aligned RMSE: 0.137622 m
- OpenVINS RPE translation RMSE: 0.004873 m

Observed behavior:

- ORB-SLAM3 repeatedly reported not enough motion for initializing and map reset messages, but the controlled rerun completed and saved full-frame and keyframe trajectories.
- OpenVINS produced an estimate and timing log, but again ended with the shutdown LibraryUnloadException.
- OpenVINS used bag_start=5 seconds.

Interpretation:

- ORB-SLAM3 had the better aligned APE on MH_03_medium in this benchmark.
- Both systems show evidence of initialization sensitivity, but the symptoms differ: ORB-SLAM3 logs repeated map resets, while OpenVINS produces a trajectory but exits with a shutdown exception.
- The RPE values are close, suggesting local motion estimation was comparable while global alignment quality differed.

### MH_05_difficult

MH_05_difficult is the stress case in the current benchmark.

Observed metrics:

- ORB-SLAM3 APE SE(3)-aligned RMSE: 0.075237 m
- ORB-SLAM3 RPE translation RMSE: 0.005066 m
- OpenVINS APE SE(3)-aligned RMSE: 0.242839 m
- OpenVINS RPE translation RMSE: 0.004271 m

Observed behavior:

- ORB-SLAM3 reported not enough acceleration, a reset caused by a bad IMU flag, and 109 frames set to lost.
- Despite those warnings, ORB-SLAM3 saved full-frame and keyframe trajectories.
- OpenVINS produced estimate and timing files, but ended with the same shutdown LibraryUnloadException.
- OpenVINS had the worst aligned APE on this sequence among the benchmark runs.

Interpretation:

- MH_05_difficult is the strongest failure-atlas example so far.
- ORB-SLAM3 clearly struggled during initialization/tracking but recovered enough to produce a trajectory.
- OpenVINS showed larger aligned trajectory error while maintaining similar local RPE magnitude.
- This sequence should be used in the README and demo to explain why accuracy tables alone are not enough.

## Cross-system comparison

- ORB-SLAM3 had lower SE(3)-aligned APE RMSE on all three benchmark sequences.
- OpenVINS had competitive RPE on MH_01_easy and MH_05_difficult, but higher aligned APE.
- ORB-SLAM3 failure symptoms appeared as initialization resets, map resets, bad IMU flag messages, and lost frames.
- OpenVINS failure/engineering symptoms appeared as repeatable ROS shutdown exceptions after saving outputs.
- Current runtime numbers should be treated as logged run times, not a fair speed benchmark.

## Future extensions

- Add exact timestamped event markers to the error timeline plots when logs expose reliable event timestamps.
- Add a third backend such as Basalt or VINS-Fusion.
- Add demo media combining camera frames, trajectories, error timelines, and failure-event cards.
- Investigate whether the OpenVINS shutdown exception is caused by ROS image transport plugin unload behavior.
