$(function(){new Vue({el:"#loginForm",data:{username:"",password:"",hasSubmission:!1,error:void 0},methods:{onSubmit:function(){this.error=void 0,this.hasSubmission=!0;var s={username:this.username,password:this.password};$.post(HOST+"/users/authenticate",JSON.stringify(s),function(s){s.status?(sessionStorage.setItem("token",s.token),location.href="mydiary.html"):this.error=s.error,this.hasSubmission=!1}.bind(this))}}})});