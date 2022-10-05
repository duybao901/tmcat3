import './App.css';
import FaceModel from './components/FaceModel/FaceModel';

function App() {
  return (
    <div className="App">
      <div style={{ padding: "50px" }}>
        <div>
          <h1 style={{ marginBottom: "40px" }}>
            Face Authentication using ReactJS
          </h1>
        </div>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <button className='btn' style={{ marginRight: '10px' }}>Face register</button>
          <button className='btn'>Face sign in</button>
        </div>
        <FaceModel></FaceModel>
      </div>
    </div>
  );
}

export default App;
