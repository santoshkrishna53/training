import { Component, OnInit } from '@angular/core';
import { ApiService } from '../shared/services/api.service';
import { AuthserviceService } from '../shared/services/authservice.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {
  file: File = null;
  email: string = '';
  data_loaded = false
  displayedColumns: string[] = ['position', 'name'];
  dataSource =  [];

  constructor(private api: ApiService,private auth: AuthserviceService) {
    if(JSON.parse(sessionStorage.getItem('user')) != null){
      this.email = JSON.parse(sessionStorage.getItem('user'))['email']
    }
    
    this.get_uploaded_documents();
   }

  ngOnInit(): void {
  }
  fileSelectes(event){
    this.file = event.target.files[0]
    this.UploadFile()
  }
  get_uploaded_documents(){
    var form = new FormData();
    form.append("email",this.email)
    this.api.get_files_authorized(form).subscribe( resp => {
      
      var docs = resp['docs']
      var i=0;
      docs.forEach((element,i) => {
        this.dataSource.push(
          {
            'position' : i,
            'name' : element['filename']
          }
        )
        
      });
      this.data_loaded = true

    })
  }
  UploadFile(){
    var form = new FormData();
    
    form.append("file", this.file , this.file.name)
    form.append("filename",this.file.name)
    if(this.file.type == 'application/json'){
      this.api.upload_document(form).subscribe(
        (res)=>{
          if(res['status'] == "success"){
            alert('document uploaded')
            this.get_uploaded_documents()
          }
          else{
            alert('failed')
          }
          
        }
      )

    }
    else{
      alert("please enter a json file")
    }
    
    
  }
  logout(){
    this.auth.SignOut();
  }

}
