import React, { Component } from "react";
import axios from "axios";

class Id extends Component {
    constructor(props) {
        super(props);
    }
    
    render() {
        return (
            <div>
                <h2>Create or change your ID here</h2>
                <p>Current ID: {this.props.currId}</p>
                <form onSubmit={this.props.handleIdSubmit}>
                    <input
                        type='text'
                        placeholder='ID'
                        value={this.props.updateField}
                        onChange={this.props.handleIdChange}
                    />
                </form>
            </div>
        )
    }
}

export default Id;