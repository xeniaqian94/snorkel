Here are a few steps related to data processing. Specifically, to load gold segments, regroup them into pseudo docs and let Snorkel run and validate any Labeling Functions (LFs), or learn a generative model from them. 

1. Create gold segments in the format of `[segment]\t[label]\t[docid]`

from one of the two types of annotation, 1) order ignorant; 2) order preserving. 

1) For order ignorant, we arbitrarily regroup segments by their labels, ignoring their original position in the paper. 

Recommended commands to run:

a. `python segment_label_2K_paper_comma_concatenated.py annotations_label-level_all-to-date-2018-4-25-WithTitle.csv`

This command will likely print out a line like `valid_title_count  2071`.

This will create a file, renamed as `annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_level_1.csv` in the format of [segment_text]\t[segment_name]\t[docid].
	
b. `python segment_label_2K_paper_comma_concatenated.py annotations_label-level_all-to-date-2018-4-25-WithTitle.csv 1 Filtered_MLD_RI_HCI_CSD_LTI_ISR.csv`

This command will likely print out a line like `valid_title_count  480`.

This will create a file, renamed as `annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_level_1.csv` in the format of [segment_text]\t[segment_name]\t[docid].

2) For order preserving, we create order-preserving label-level gold segments using the ipynb `make-pseudo-docs.ipynb` from parent directory. The resulting gold segments for level 1 is `annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled.originalSegments_level1.csv` file in the format of [segment_text],[segment_name],[docid]. For level 2 is `annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled.originalSegments_level2.csv`


2. Regroup segments into pseudo docs:

1) For order ignorant, we regroup all segments in the order of ["background","purpose","finding","mechanism","method"].

	python regroup_groundtruth_2K_paper_order_ignorant.py annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_level_1.csv 
	
	python regroup_groundtruth_2K_paper_order_ignorant.py annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_level_2.csv 

2) For order preserving, we regroup all segments in their original order, separated by ~(tilde), finally closed by a .(period). This also requires us to change the Test_Run_8_Calculating_Coverage_and_Position_Aware_LF.ipynb. Specifically, we need a non_tilde_matcher instead of a non_comma_matcher. 

    python regroup_groundtruth_2K_paper_order_preserving.py annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled.originalSegments_level_1.csv

    python regroup_groundtruth_2K_paper_order_preserving.py annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled.originalSegments_level_2.csv


This will gets you `annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_regrouped.originalSegments_level_1.csv` and `annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_regrouped.originalSegments_level_2.csv`.

3. Concatenate three files together, train/dev/test set

70K papers plus 10 cscw paper samples are in 70kpaper_061418_cleaned_noBookLecture

1) For order ignorant, 

2K groundtruth are in `annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_regrouped_level_[1/2].csv`

Concatenated 70K + 10 cscw + 2K are in `70kpaper_061418_cleaned_noBookLecture_10cscw_2k.tsv`

Command:    
    cat 70kpaper_061418_cleaned_noBookLecture_10cscw.tsv annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_regrouped_level_1.csv annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_regrouped_level_2.csv     > 70kpaper_061418_cleaned_noBookLecture_10cscw_2k.tsv

2) For order preserving, 

2K groundtruth are in `annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_regrouped.originalSegments_level_[1/2].csv`

Concatenated 70K + 10 cscw + 2K are in `70kpaper_061418_cleaned_noBookLecture_10cscw_2k.tsv`

Command:    
    cat 70kpaper_061418_cleaned_noBookLecture_10cscw.tsv annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_regrouped.originalSegments_level_1.csv annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_regrouped.originalSegments_level_2.csv     > 70kpaper_061418_cleaned_noBookLecture_10cscw_2k_order_preserving.tsv


