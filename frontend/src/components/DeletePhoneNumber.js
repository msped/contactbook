import React, { Component, Fragment } from 'react'
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import { Button, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions } from '@mui/material'
import api from '../axios'

export default class DeletePhoneNumber extends Component {

    constructor(props){
        super(props)
        this.state = {
            PhoneNumberID: props.PhoneNumberID,
            open: false
        }
    }

    handleToggle = () => {
        this.setState({ open: !this.state.open })
    }

    handleDelete = () => {
        api.delete(
            '/contacts/phone-number/' + this.state.PhoneNumberID
        )
        .then((res) => {
            // use res to provide action
            this.props.RemoveRow(this.state.PhoneNumberID)
            this.setState({ open: false })
        })
        .catch((err) => {
            console.log(err)
        })
    }

    render() {
        return (
            <Fragment>
                <Button variant="contained" color="error" onClick={this.handleToggle}>
                    <DeleteForeverIcon fontSize='small'/>
                </Button>

                <Dialog
                    open={this.state.open}
                    onClose={this.handleClose}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"
                >
                    <DialogTitle id="alert-dialog-title">
                    {"Are you sure?"}
                    </DialogTitle>
                    <DialogContent>
                        <DialogContentText id="alert-dialog-description">
                            If you delete this item, you will not be able to get it back. 

                            Are you sure you want to delete this phone number?
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleToggle}>Cancel</Button>
                        <Button onClick={this.handleDelete} autoFocus>
                            Delete
                        </Button>
                    </DialogActions>
                </Dialog>
            </Fragment>
        )
    }
}
