function showLoader() {
    document.getElementById("loader_id").style.display = "block";
    }
function alertTranscriptStatus() {
    transcript_status = document.getElementById("transcript_status_id").innerHTML;
    if (transcript_status.length > 0){
        alert(transcript_status);
    }
}
function alertTranscriptDownloadUploadFileStatus(){
    transcript_download_file_status = document.getElementById("transcript_download_file_status_id").innerHTML;
    transcript_upload_file_status = document.getElementById("transcript_upload_file_status_id").innerHTML;
    if (transcript_download_file_status.length > 0){
        alert(transcript_download_file_status);
    }
    if (transcript_upload_file_status.length > 0){
        alert(transcript_upload_file_status);
    }
}
function assignTrasnscriptDownloadFileName(){
    var dropdown_transcript_files = document.getElementById("dropdown_transcript_files_id");
    var dropdown_transcript_file = dropdown_transcript_files.options[dropdown_transcript_files.selectedIndex].text;
    document.getElementById("download_file_name_id").value = dropdown_transcript_file;
}
function assignSelectedTranscriptFileName(){
    var dropdown_transcript_files = document.getElementById("dropdown_transcript_files_id");
    var dropdown_transcript_file = dropdown_transcript_files.options[dropdown_transcript_files.selectedIndex].text;
    document.getElementById("selected_source_text_file_id").innerHTML = dropdown_transcript_file.toUpperCase();
}
function assignSelectedPromptFileName(){
    var dropdown_prompt_files = document.getElementById("dropdown_prompt_files_id");
    var dropdown_prompt_file = dropdown_prompt_files.options[dropdown_prompt_files.selectedIndex].text;
    document.getElementById("selected_prompt_file_id").innerHTML = dropdown_prompt_file.toUpperCase();
}
function assignPromptDownloadFileName(){
    var dropdown_prompt_files = document.getElementById("dropdown_prompt_files_id");
    var dropdown_prompt_file = dropdown_prompt_files.options[dropdown_prompt_files.selectedIndex].text;
    document.getElementById("download_file_name_id").value = dropdown_prompt_file;
}
function alertPromptDownloadUploadFileStatus(){
    prompt_download_file_status = document.getElementById("prompt_download_file_status_id").innerHTML;
    prompt_upload_file_status = document.getElementById("prompt_upload_file_status_id").innerHTML;
    output_file_status_id = document.getElementById("output_file_status_id").innerHTML;
    if (prompt_download_file_status.length > 0){
        alert(prompt_download_file_status);
    }
    if (prompt_upload_file_status.length > 0){
        alert(prompt_upload_file_status);
    }
    if (output_file_status_id.length > 0){
        alert(output_file_status_id);
    }
}
function assignSelectedFileName(){
    document.getElementById("selected_source_text_file_value_id").value = document.getElementById("selected_source_text_file_id").innerHTML;
    document.getElementById("selected_prompt_file_value_id").value = document.getElementById("selected_prompt_file_id").innerHTML;
}
function assignOutputDownloadFileName(){
    var dropdown_output_files = document.getElementById("dropdown_output_files_id");
    var dropdown_output_file = dropdown_output_files.options[dropdown_output_files.selectedIndex].text;
    document.getElementById("download_file_name_id").value = dropdown_output_file;
}
function alertOutputDownloadFileStatus(){
    output_download_file_status = document.getElementById("output_download_file_status_id").innerHTML;
    if (output_download_file_status.length > 0){
        alert(output_download_file_status);
    }
}