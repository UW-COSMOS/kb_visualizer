#!/bin/sh

if [ -z $PG_CONN_STR ];
then
    echo "Please provide a conn string"
    exit 1
else
    echo $PG_CONN_STR
fi

echo "Creating tmp tables and importing data to schema $1"

psql "$PG_CONN_STR" -c "CREATE TABLE IF NOT EXISTS $1.output_tmp (
        document_name text,
        id int, 
        text text,
        document_id int,
        equation_id int,
        equation_text text,
        equation_offset text, 
        sentence_id int,
        sentence_offset int,
        sentence_text text,
        score float,
        var_top	int,
        var_bottom int,
        var_left int,
        var_right int,
        var_page int,
        sent_xpath text,
        sent_words text[],
        sent_top text[],
        sent_table_id int,
        sent_section_id int,
        sent_row_start int,
        sent_row_end int,
        sent_right int[],
        sent_position int,
        sent_pos_tags text[],
        sent_paragraph_id int,
        sent_page int[],
        sent_ner_tags text[],
        sent_name text,
        sent_lemmas text[],
        sent_left int[],
        sent_html_tag text,
        sent_html_attrs text[],
        sent_document_id int,
        sent_dep_parents text[],
        sent_dep_labels text[],
        sent_col_start int,
        sent_col_end int,
        sent_char_offsets int[],
        sent_cell_id int,
        sent_bottom int[],
        sent_abs_char_offsets int[],
        equation_top int,
        equation_bottom	int,
        equation_left int,
        equation_right int,
        equation_page int,
        equation_text_duplicate text,
        symbols text[],
        phrases text[],
        phrases_top text[],
        phrases_bottom text[],
        phrases_left text[],
        phrases_right text[],
        phrases_page text[],
        sentence_img text,
        equation_img text,
        UNIQUE (document_name, id)
        );

CREATE TABLE IF NOT EXISTS $1.figures_tmp (
        target_img_path text,
        target_unicode text,
        target_tesseract text,
        assoc_img_path text,
        assoc_unicode text,
        assoc_tesseract text,
        html_file text,
        UNIQUE (target_img_path)
        );

CREATE TABLE IF NOT EXISTS $1.tables_tmp (
        target_img_path text,
        target_unicode text,
        target_tesseract text,
        assoc_img_path text,
        assoc_unicode text,
        assoc_tesseract text,
        html_file text,
        UNIQUE (target_img_path)
        );"

psql "$PG_CONN_STR" -c "\\copy $1.figures_tmp(
        target_img_path,
        target_unicode,
        target_tesseract,
        assoc_img_path,
        assoc_unicode,
        assoc_tesseract,
        html_file) FROM  '$(pwd)/output/figures.csv' DELIMITER ',' CSV HEADER;"

psql "$PG_CONN_STR" -c "INSERT INTO $1.figures SELECT * FROM $1.figures_tmp ON CONFLICT DO NOTHING; DROP TABLE $1.figures_tmp;"

psql "$PG_CONN_STR" -c "\\copy $1.tables_tmp(
        target_img_path,
        target_unicode,
        target_tesseract,
        assoc_img_path,
        assoc_unicode,
        assoc_tesseract,
        html_file) FROM  '$(pwd)/output/tables.csv' DELIMITER ',' CSV HEADER;"

psql "$PG_CONN_STR" -c "INSERT INTO $1.tables SELECT * FROM $1.tables_tmp ON CONFLICT DO NOTHING; DROP TABLE $1.tables_tmp;"

# copy from output/output.csv

psql "$PG_CONN_STR" -c "\\copy $1.output_tmp(
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
var_top,
var_bottom,
var_left,
var_right,
var_page,
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
equation_top,
equation_bottom,
equation_left,
equation_right,
equation_page,
equation_text_duplicate,
symbols,
phrases,
phrases_top,
phrases_bottom,
phrases_left,
phrases_right,
phrases_page,
sentence_img,
equation_img
) FROM '$(pwd)/output/output.csv' DELIMITER ',' CSV HEADER;"


psql "$PG_CONN_STR" -c "INSERT INTO $1.output SELECT * FROM $1.output_tmp ON CONFLICT DO NOTHING; DROP TABLE $1.output_tmp; REFRESH MATERIALIZED VIEW $1.sentence; REFRESH MATERIALIZED VIEW $1.variable; REFRESH MATERIALIZED VIEW $1.phrase;"
