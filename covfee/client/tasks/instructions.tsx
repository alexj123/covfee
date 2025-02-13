import * as React from 'react'
import {
    Row,
    Col,
} from 'antd'
import { InstructionsTaskSpec } from '@covfee-types/tasks/instructions'
import { MarkdownLoader } from './utils/markdown_loader'
import { BasicTaskProps, CovfeeTask } from './base'
import { TaskType } from '@covfee-types/task'
import { Form } from '../input/form'

interface Props extends TaskType, BasicTaskProps {
    spec: InstructionsTaskSpec
}

interface State {
    form: {
        values: any
    }
}

export class InstructionsTask extends CovfeeTask<Props, State> {

    state: State = {
        form: {
            values: null
        }
    }

    constructor(props: Props) {
        super(props)
        if(props.response && props.response.data)
            this.state.form.values = props.response.data
    }

    handleSubmit = (values: any) => {
        // let vals = this.state.form.values
        // if(!vals || !vals.length) vals = null
        
        this.props.onSubmit(this.state.form.values, null, true)
    }

    handleFormChange = (values: any) => {
        this.setState({
            form: {
                ...this.state.form,
                values: {
                    ...this.state.form.values,
                    ...values
                }
            }
        })
    }

    render() {
        return <Row style={{margin: '2em 0'}}>
            <Col sm={{span:22, offset:1}} md={{span: 20, offset: 2}} lg={{span:16, offset: 4}} xl={{span: 14, offset: 5}}>
                <MarkdownLoader content={this.props.spec.content}/>
                <Form {...this.props.spec.form}
                        disabled={this.props.disabled}  
                        values={this.state.form.values} 
                        setValues={this.handleFormChange}
                        withSubmitButton={true}
                        renderSubmitButton={this.props.renderSubmitButton}
                        onSubmit={this.handleSubmit}/>
            </Col>
        </Row>
    }
}

export { MarkdownLoader}
export default InstructionsTask