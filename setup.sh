if [ -z $PG_CONN_STR ];
then
    echo "Please provide a conn string"
    exit 1
else
    echo $PG_CONN_STR
fi

psql "$PG_CONN_STR" -f schema.sql


psql "$PG_CONN_STR" -c "\\copy figures(
        target_img_path,
        target_unicode,
        target_tesseract,
        assoc_img_path,
        assoc_unicode,
        assoc_tesseract,
        html_file) FROM  '$(pwd)/output/figures.csv' DELIMITER ',' CSV HEADER;"

psql "$PG_CONN_STR" -c "\\copy tables(
        target_img_path,
        target_unicode,
        target_tesseract,
        assoc_img_path,
        assoc_unicode,
        assoc_tesseract,
        html_file) FROM  '$(pwd)/output/tables.csv' DELIMITER ',' CSV HEADER;"

# copy from output/output.csv

psql "$PG_CONN_STR" -c "\\copy output(
document_name,
id, 
text,
document_id,
equation_id,
equation_text,
equation_offset, 
sentence_id,
sentence_offset,
sentence_text,
score,
sent_xpath,
sent_words,
sent_top,
sent_table_id,
sent_section_id,
sent_row_start,
sent_row_end,
sent_right,
sent_position,
sent_pos_tags,
sent_paragraph_id,
sent_page,
sent_ner_tags,
sent_name,
sent_lemmas,
sent_left,
sent_html_tag,
sent_html_attrs,
sent_document_id,
sent_dep_parents,
sent_dep_labels,
sent_col_start,
sent_col_end,
sent_char_offsets,
sent_cell_id,
sent_bottom,
sent_abs_char_offsets,
equation_variables,
symbols,
phrases,
phrases_top,
phrases_bottom,
phrases_left,
phrases_right,
phrases_page,
symbols_top,
symbols_bottom,
symbols_left,
symbols_right,
symbols_page,
sentence_img,
equation_img) FROM '$(pwd)/output/output.csv' DELIMITER ',' CSV HEADER;"
