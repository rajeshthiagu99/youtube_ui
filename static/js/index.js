function saveFileName(){
    download_file_name = document.getElementById("download_file_name_id").value;
    localStorage.setItem("download_file_name", download_file_name);
}
// ==============================transcript_files.html, gpt_text_workshop.html and output_file_library.html==============================

function showLoader(){
    document.getElementById("loader_id").style.display = "block";
}
function alertTranscriptStatus(){
    const transcript_status = document.getElementById("transcript_status_id");
    transcript_status.style.display = "block";
    setTimeout(() => {
    transcript_status.style.display = "none";
    }, 5000);
}
// ==============================create_transcript.html==============================

function assignTrasnscriptDownloadFileName(){
    var dropdown_transcript_files = document.getElementById("dropdown_transcript_files_id");
    var dropdown_transcript_file = dropdown_transcript_files.options[dropdown_transcript_files.selectedIndex].text;
    document.getElementById("download_file_name_id").value = dropdown_transcript_file;
}
function downloadUploadTranscriptFile(){
    data=document.getElementById("transcript_file_content_id").value;
    document.getElementById("transcript_file_content_id").value = "";
    if (data.length > 0){
        let download_file_name = localStorage.getItem("download_file_name");
        if(download_file_name){
            var file = new Blob([data], { type: 'text/plain' });
            var a = document.createElement("a"),
                url = URL.createObjectURL(file);
            a.href = url;
            a.download = download_file_name;
            document.body.appendChild(a);
            a.click();
            setTimeout(function() {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);  
            }, 0); 
        }
    }

    const transcript_upload_file_status = document.getElementById("transcript_upload_file_status_id");
    if (transcript_upload_file_status.innerHTML.length > 0){
        transcript_upload_file_status.style.display = "block";
        setTimeout(() => {
        transcript_upload_file_status.style.display = "none";
        }, 5000);
    }
}
// ==============================transcript_files.html==============================

function assignPromptDownloadFileName(){
    var dropdown_prompt_files = document.getElementById("dropdown_prompt_files_id");
    var dropdown_prompt_file = dropdown_prompt_files.options[dropdown_prompt_files.selectedIndex].text;
    document.getElementById("download_file_name_id").value = dropdown_prompt_file;
}
function assignSelectedFileName(){

    var dropdown_transcript_files = document.getElementById("dropdown_transcript_files_id");
    var dropdown_transcript_file = dropdown_transcript_files.options[dropdown_transcript_files.selectedIndex].text;

    var dropdown_prompt_files = document.getElementById("dropdown_prompt_files_id");
    var dropdown_prompt_file = dropdown_prompt_files.options[dropdown_prompt_files.selectedIndex].text;

    document.getElementById("selected_source_text_file_value_id").value = dropdown_transcript_file;
    document.getElementById("selected_prompt_file_value_id").value = dropdown_prompt_file;
}
function alertDownloadUploadOutputStatus() {
    data=document.getElementById("prompt_file_content_id").value;
    document.getElementById("prompt_file_content_id").value = "";
    if (data.length > 0){
        let download_file_name = localStorage.getItem("download_file_name");
        if(download_file_name){
            var file = new Blob([data], { type: 'text/plain' });
            var a = document.createElement("a"),
                url = URL.createObjectURL(file);
            a.href = url;
            a.download = download_file_name;
            document.body.appendChild(a);
            a.click();
            setTimeout(function() {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);  
            }, 0); 
        }
    }

    const prompt_upload_file_status = document.getElementById("prompt_upload_file_status_id");
    if (prompt_upload_file_status.innerHTML.length > 0){
        prompt_upload_file_status.style.display = "block";
        setTimeout(() => {
        prompt_upload_file_status.style.display = "none";
        }, 5000);
    }

    const output_file_status = document.getElementById("output_file_status_id");
    if (output_file_status.innerHTML.length > 0){
        output_file_status.style.display = "block";
        setTimeout(() => {
        output_file_status.style.display = "none";
        }, 5000);
    }
}
// ==============================gpt_text_workshop.html==============================

function assignOutputDownloadFileName(){
    var dropdown_output_files = document.getElementById("dropdown_output_files_id");
    var dropdown_output_file = dropdown_output_files.options[dropdown_output_files.selectedIndex].text;
    document.getElementById("download_file_name_id").value = dropdown_output_file;
}
function downloadOutputFile() {
    data=document.getElementById("output_file_content_id").value;
    document.getElementById("output_file_content_id").value = "";
    if (data.length > 0){
        let download_file_name = localStorage.getItem("download_file_name");
        if(download_file_name){
            var file = new Blob([data], { type: 'text/plain' });
            var a = document.createElement("a"),
                url = URL.createObjectURL(file);
            a.href = url;
            a.download = download_file_name;
            document.body.appendChild(a);
            a.click();
            setTimeout(function() {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);  
            }, 0); 
        }
    }
}
// ==============================output_file_library.html==============================