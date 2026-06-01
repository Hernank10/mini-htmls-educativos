let recorder, stream;
async function toggleRecording(){
  if(!recorder){
    try{
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      recorder = new MediaRecorder(stream);
      const chunks = [];
      recorder.ondataavailable = e => chunks.push(e.data);
      recorder.onstop = async ()=>{
        const blob = new Blob(chunks, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = 'recording.webm'; a.click();
        stream.getTracks().forEach(t=>t.stop());
        recorder = null;
        alert('Grabación lista para subir (archivo descargado).');
      };
      recorder.start();
      alert('Grabando... pulsa de nuevo para detener');
    }catch(err){
      alert('No se pudo acceder al micrófono: ' + err.message);
    }
  } else {
    recorder.stop();
  }
}