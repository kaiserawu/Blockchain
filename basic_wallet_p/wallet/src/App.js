import React, {Component} from 'react';
import './App.css';
import Id from './components/id';

import axios from 'axios';


class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            id: '',
            updateField: ''
        }

        this.handleIdSubmit = this.handleIdSubmit.bind(this);
        this.handleIdChange = this.handleIdChange.bind(this);
    }

    handleIdSubmit = e => {
        e.preventDefault();
        console.log('submitting');
        this.setState(prevState => {
            return {
                id: prevState.updateField,
                updateField: ''
            }
        })
    }
    handleIdChange = e => {
        this.setState({
            updateField: e.target.value
        })
    }

    render() {
        return (
            <div className="App">
                <Id
                    currId={this.state.id}
                    updateField={this.state.updateField}
                    handleIdSubmit={this.handleIdSubmit}
                    handleIdChange={this.handleIdChange}
                />
            </div>
        );
    }
}

export default App;
