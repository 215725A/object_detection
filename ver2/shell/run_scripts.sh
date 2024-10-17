source .env

source ~/.bashrc_conda
conda activate lab_env

echo "Stdout log path: $STDOUT_LOG_PATH"

start_time=$(date +%s)

scripts=("detect_road.py" "projective_transfromation.py" "detect.py")

for script in ${scripts[@]}
do
  echo "実行中: ptyhon/$script"
  script_start_time=$(date +%s)
  python "$script" -c ${YML_PATH}
  script_end_time=$(date +%s)
  script_duration=$((script_end_time - script_start_time))
  echo "実行終了: $script"
  echo "スクリプト実行にかかった時間: $script_duration 秒"
  echo ""
done

end_time=$(date +%s)

total_duration=$((end_time - start_time))
convert_seconds() {
  local total_seconds=$1
  local minutes=$(( (total_seconds % 3600) / 60 ))
  local seconds=$((total_seconds % 60))
  printf "%02d:%02d\n" $minutes $seconds
}

echo "全体のスクリプト実行にかかった時間: $(convert_seconds $total_duration)"