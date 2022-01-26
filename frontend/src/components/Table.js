import React, { Component } from 'react'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import DeletePhoneNumber from '../components/DeletePhoneNumber'
import DeleteEmail from '../components/DeleteEmail'

import getType from '../utils'

export default class ContentTable extends Component {

    constructor(props) {
        super(props)
        this.state = {
            items: props.items,
            table: props.table
        }
        this._isMounted = false
    }

    componentDidMount() {
        this._isMounted = true
    }

    handleRemoveOfRow = (phoneNumberID) => {
        const newState = [...this.state.items]
        console.log("State before Splice ", newState)
        const index = newState.findIndex(key => key.id === phoneNumberID)
        newState.splice(index, 1)
        this.setState({ items: newState })
        console.log("State After Splice ", this.state.items)
    }
    
    render() {
        const { items, table } = this.state

        return (
            <TableContainer component={Paper}>
                <Table aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell style={{ width: '40%' }}>{table}</TableCell>
                            <TableCell style={{ width: '40%' }} align="center">Type</TableCell>
                            <TableCell style={{ width: '10%' }} align="center"></TableCell>
                            <TableCell style={{ width: '10%' }} align="center"></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                    {items.map((row) => (
                        <TableRow
                            key={row.id}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">{row.data}</TableCell>
                                <TableCell align="center">
                                    {getType(row.type)}
                                </TableCell>
                                <TableCell align="center">{
                                    table === "Numbers" ? 
                                        <DeletePhoneNumber PhoneNumberID={row.id} RemoveRow={this.handleRemoveOfRow}/>
                                    :
                                        <DeleteEmail EmailID={row.id} RemoveRow={this.handleRemoveOfRow}/>
                                }</TableCell>
                                <TableCell align='center'></TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
            </TableContainer>
        )
    }
}
