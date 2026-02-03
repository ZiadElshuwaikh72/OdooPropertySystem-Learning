/* @odoo-module */

import { Component ,useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { FormView } from "@app_one/components/formView/formView";

export class ListViewAction extends Component {
    static template = "app_one.ListView";
    static components= { FormView };

    setup(){
        this.state=useState({
         records :[],
        showCreateForm: false,
        });
        this.orm=useService("orm");
        this.rpc=useService("rpc");
        this.loadRecords();

        this.intervalId=setInterval(()=>{this.loadRecords()},3000);
        onWillUnmount(()=>{clearInterval(this.intervalId)});

        this.onRecordCreated=this.onRecordCreated.bind(this);
    }
        //  method use service ORM
//   async loadRecords(){
//       const result = await this.orm.searchRead("property",[],[]);
//       this.state.records=result;
//    }

        //  method use service RPC . as read from CRUD
    async loadRecords(){
        const result= await this.rpc(
        "/web/dataset/call_kw",{
        model:"property",
        method:"search_read",
        args:[[]],
        kwargs:{ fields :['id','name','postcode','date_availability','expected_price']}
        });
           // console.log(result);
        this.state.records=result;
    }
    //  method use service RPC . as create from CRUD
    async createRecords(){
        await this.rpc("/web/dataset/call_kw",{
        model:"property",
        method:"create",
        args:[{
            name:"new property static ",
            postcode:"10102",
            date_availability:"2026-02-01"
        }],
        kwargs:{}
        });
        this.loadRecords();
    }
    //  method use service RPC . as unlink or delete from CRUD
    async deleteRecords(record_Id){
        await this.rpc("/web/dataset/call_kw",{
        model:"property",
        method:"unlink",
        args:[record_Id],
        kwargs:{}
        });
        this.loadRecords();
    }
    // method check flag as true or false on button open form view
    toggleCreateForm(){

        this.state.showCreateForm = ! this.state.showCreateForm
    }
    //method close form view while click button save  and load records
    onRecordCreated(){
        this.state.showCreateForm=false;
        this.loadRecords();
    }
}

registry.category("actions").add("app_one.action_list_view",ListViewAction);
