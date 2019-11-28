import React, { Component } from 'react';
import {Row, Col} from 'antd'
import { post } from 'axios';
import './App.css';


class App extends Component {
  state = {
    videos: [],
    selectedVideo: "",
    validationError: "",
    face_confidence: "",
    object_confidence: "",}

  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.onFormSubmit = this.onFormSubmit.bind(this)
    this.onChange = this.onChange.bind(this)
    this.fileUpload = this.fileUpload.bind(this)
    this.handleFaceChange = this.handleFaceChange.bind(this);
    this.handleObjectChange = this.handleObjectChange.bind(this);
    this.handleConfigSubmit = this.handleConfigSubmit.bind(this);
  }

  componentDidMount() {
    let headers = new Headers();

    headers.append('Access-Control-Allow-Origin', 'http://localhost:3000');
    headers.append('Access-Control-Allow-Credentials', 'true');

    fetch("http://localhost:5000/video",{
       // mode: 'no-cors'
    })
    .then(response => {
      return response.json();
    })
    .then(data => {
      let videosFromApi = data.map(video => { return {value: video.id, display: video.filename} })
      this.setState({ videos: [{video: '', display: 'Select a video to start'}].concat(videosFromApi) });

      //this.setState({
      //  videos: data
      //})
    }).catch(error => {
      console.log(error);
    });

    fetch("http://localhost:5000/config",{
       // mode: 'no-cors'
    })
    .then(response => {
      return response.json();
    })
    .then(data => {
      this.setState({
        face_confidence: data.face_confidence,
        object_confidence: data.object_confidence
      })
    }).catch(error => {
      console.log(error);
    });
  }

  handleConfigSubmit(e) {
    e.preventDefault() // Stop form submit
    fetch('http://localhost:5000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
      },
      body: JSON.stringify({ 
        "face_confidence": this.state.face_confidence, 
        "object_confidence":this.state.object_confidence}),
    })
    .then(response => response.json())
    .catch(error =>{
        console.log(error)
    })
    alert("Config has been amended!");
    window.location.reload();
  }

  handleFaceChange(event) {
    this.setState({face_confidence: event.target.value});
  }
  handleObjectChange(event) {
    this.setState({object_confidence: event.target.value});
  }

  handleClick() {
    console.log('this is:', this);
  }
  onFormSubmit(e){
    e.preventDefault() // Stop form submit

    this.fileUpload(this.state.file).then((response)=>{
      console.log(response.data);
      if (alert("Video has been uploaded!")) {}
        else window.location.reload();
    }).catch(error =>{
        console.log(error)
    })
  }
  onChange(e) {
    this.setState({file:e.target.files[0]})
  }
  fileUpload(file){
    const url = 'http://localhost:5000/video';
    const formData = new FormData();
    formData.append('video',file)
    const config = {
        headers: {
            'content-type': 'multipart/form-data'
        }
    }
    return  post(url, formData,config)
  }

  render() {
    const videoURL = "http://localhost:5000/video_feed/" + this.state.selectedVideo
    return (
    <div className="App">
      
          <h1>Video Streaming Demonstration</h1>
          <hr className="seperator1"/>
          <div className = "leftbox">
            <form className="cell" onSubmit={this.onFormSubmit}>
              <input className = "field" type="file" onChange={this.onChange} accept=".mp4,.flv,.mkv"/>
              <div><button className="btn" type="submit">Upload Video</button></div>
            </form>
          </div>

          <div className = "middlebox">
           <form onSubmit={this.handleConfigSubmit}>
            <div className = "cell">Face Confidence Threshold: </div>
            <input className = "field" type="text" value={this.state.face_confidence} onChange={this.handleFaceChange} />
            <div className = "cell">Object Confidence Threshold:</div>
            <input className = "field" type="text" value={this.state.object_confidence} onChange={this.handleObjectChange} />
            <input type="submit" value="Amend" />
          </form>
          </div>

          <div className = "rightbox">
            <div className = "cell">Video List:</div> 
            <select className = "cell" value={this.state.selectedVideo} 
                onChange={(e) => this.setState({selectedVideo: e.target.value, validationError: e.target.value === "" ? "You must select your favourite team" : ""})}>
                {this.state.videos.map((video) => <option key={video.value} value={video.value}>{video.display}</option>)}
            </select>
          </div>

          <hr className="seperator1"/>
          <br/>

          {this.state.selectedVideo!=='' ? 
          <div>
            <img src={videoURL}/>
          </div> : ''}
          
        
    </div>
    );
  }
}

export default App;
