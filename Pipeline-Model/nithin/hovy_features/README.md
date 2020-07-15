python3 -m spacy init-model en model/en_vectors_wiki_lg --vectors-loc wiki-news-300d-1M.vec

python3 col_header_qtype_sim.py -qt train_q_type.csv -tf ../../data/tables/test/transposed_csvs/ -o train_col_qtype_sim.csv
python3 col_header_qtype_sim.py -qt test_q_type.csv -tf ../../data/tables/test/transposed_csvs/ -o test_col_qtype_sim.csv
python3 col_header_qtype_sim.py -qt seeded_qtype_dev.csv -tf ../../data/tables/test/transposed_csvs/ -o seeded_dev_col_qtype_sim.csv
python3 col_header_qtype_sim.py -qt seeded_qtype_train.csv -tf ../../data/tables/train/transposed_csvs/ -o seeded_train_col_qtype_sim.csv
