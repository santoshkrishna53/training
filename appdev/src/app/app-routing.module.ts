import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { AuthGuard } from './shared/guard/auth.guard';

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'home',
    component : HomeComponent,
    canActivate : [ AuthGuard ]
  },
  { path: '**', component:  LoginComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }


// {
//   path: '',
//   component: LayoutComponent,
//   canActivate: [AuthGuard],
//   children: [
//     {
//       path:'home',
//       component:HomeComponent,
//       canActivate: [AuthGuard]
//     }
//   ]
// }
