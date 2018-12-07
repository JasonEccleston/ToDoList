<template>
  <div>
    <nav class="navbar">
      <label>Jason & Marc's ToDo List</label>
      <div>
        <button class="btn btn-outline pull-right" type="button" float="right" v-on:click="goToProfile()">Profile</button>
        <button class="btn btn-outline pull-right" type="button" float="right" v-on:click="signout()">Sign Out</button>
      </div>
    </nav>
    <div class="row">
      <div class="col-2">
        <div class="side-list">
          <label>Users:</label>
          <ul class="list-group">
            <button type="button" class ="list-group-item" v-for="user in this.users" v-on:click="changeListDisplay(user.listId, user.displayName)">{{user.displayName}}</button>
          </ul>
        </div>
      </div>
      <div class="col-8">
        <div class="container">
          <label>This is a list of {{this.$cookies.get('currentUserDisplayed')}}'s current tasks:</label>
          <ul class="list-group">
            <li class ="list-group-item pull left" v-for="item in this.listItems">
              {{item.item}}
              <button class= "btn" type="button" style="float:right" v-on:click="deleteItem(item.itemId)" :disabled="editable == 0" :hidden="editable == 0">delete</button>
              <button class= "btn" style="float:right" v-on:click="editItem(item.itemId)" :disabled="editable ==0" :hidden="editable == 0">edit</button>
            </li>
          </ul>
          <div class="form-group">
            <label for="task" :disabled="editable == 0" :hidden="editable == 0">To Do:</label>
            <input type="text" maxlength="255" placeholder="New Task" class="form-control" id="task" v-model="newItem" :disabled="editable == 0" :hidden="editable == 0"></input>
          </div>
          <div>
            <button class="ht-tm-element btn" type="submit" style="float:left" v-on:click="submitItem(newItem)" :disabled="editable == 0" :hidden="editable == 0">Submit</button>
            <button class="btn" type="submit" style="float:right" v-on:click="deleteList(newItem)" :disabled="editable == 0" :hidden="editable == 0">Clear List</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data(){
      return {
        users: '',
        listItems: '',
        newItem: '',
        editable: true,
        currentUserDisplayed: '',
      }
    },
    beforeCreate: function() {
              document.body.className = 'main';
    },
    created: function() {
      if(this.$cookies.get('user')== null){
        alert("Please sign in")
        this.$router.push("/signin")
      }
      this.getUsers()
      this.getList()
    },
    methods: {
      getUsers(){
        this.$axios.get('https://info3103.cs.unb.ca:36479/users', { headers: {
          "Access-Control-Allow-Origin": '*'
        }})
        .then(response => {
          if(response.status == 200){
            this.users = response.data.users
            console.log(this.users)
          }
        }).catch(error => {
          console.log(error)
        })
      },
      signout(){
        this.$axios.delete('https://info3103.cs.unb.ca:36479/signin', { headers: {
          "Access-Control-Allow-Origin": '*'
        }})
        .then(response => {
          if(response.status == 204){
            this.$cookies.remove('user')
            this.$cookies.remove('userId')
            this.$router.push("/signin")
          }
        }).catch(error => {
          console.log(error)
        })
      },
      getList(){
        this.$axios.get('https://info3103.cs.unb.ca:36479/users/' + this.$cookies.get('userId') + '/list', { headers: {
          "Access-Control-Allow-Origin": '*'
        }})
        .then(response => {
          if(response.status == 200){
              this.listItems = response.data.listItems
          }
        }).catch(error => {
          console.log(error)
        })
      },
      changeListDisplay(listId, displayName){
        this.$axios.get('https://info3103.cs.unb.ca:36479/users/' + listId + '/list', { headers: {
          "Access-Control-Allow-Origin": '*'
        }})
        .then(response => {
          if(response.status == 200){
              if(listId == this.$cookies.get('userId')){
                this.editable = true
                this.$cookies.set('currentUserDisplayed', displayName)
                console.log(this.currentUserDisplayed)
              }
              else{
                this.$cookies.set('currentUserDisplayed', displayName)
                this.editable = false;
              }
              this.listItems = response.data.listItems
          }
        }).catch(error => {
          console.log(error)
        })
      },
      submitItem(newItem){
        if(newItem.length < 5){
          alert("Enter a task that is longer than 5 characters")
        }
        else{
          this.$axios.post('https://info3103.cs.unb.ca:36479/users/' + this.$cookies.get('userId') + '/list',
            {'item': newItem})
          .then(response => {
            this.newItem = '';
            this.getList()
            console.log(response.data);
          }).catch(error => {
            console.log(error)
          })
        }
      },
      deleteItem(itemId){
        this.$axios.delete('https://info3103.cs.unb.ca:36479/users/' + this.$cookies.get('userId') + '/list/items/' + itemId)
        .then(response => {
          this.getList()
          console.log(response.data);
        }).catch(error => {
          console.log(error)
        })
      },
      deleteList(){
        this.$axios.delete('https://info3103.cs.unb.ca:36479/users/' + this.$cookies.get('userId') + '/list')
        .then(response => {
          this.getList()
          console.log(response.data)
        }).catch(error => {
          console.log(error)
        })
      },
      editItem(itemId){
        var newItem = window.prompt("Enter the updated task:", "write here");
        if(newItem.length < 5){
          alert("length too short")
          return
        }
        console.log(newItem)
        this.$axios.put('https://info3103.cs.unb.ca:36479/users/' + this.$cookies.get('userId') + '/list/items/' + itemId,
      {"item": newItem})
        .then(response => {
          this.getList()
        }).catch(error => {
          console.log(error)
        })
      },
      goToProfile(){
        this.$router.push("/profile")
      }
    }
  }
</script>

<style scoped>

.side-list .list-group{
  overflow-y: scroll;
  overflow-x: hidden;
  min-height: 85vh;
  max-height: 85vh;
}
.side-list .list-group .list-group-item {
  background-color: white;
  min-height: 50px;
}
.side-list label {
  font-size: 20pt;
}
.side-list button{
    height: 50px;
    background-color: white;

}
.container .list-group .list-group-item {
  overflow-wrap: break-word;
  margin-top: 10px;
  border-radius: 20px;
}
.container label {
  font-size: 20pt;
}
.container .list-group .list-group-item button {
  font-size: 10pt;
}

.container button {
  background-color: #D82E3B;
  color: black;
  opacity: 1;
}

.col-8 button {
  color:white;
  border-radius: 20px;
  background-color: #D82E3B;
  border-color: #D82E3B;
}
.col-8 .form-group input {
  border-radius: 20px;
}

nav {
  background-color: #D82E3B
}
nav .btn {
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  color:white;
  border-radius: 20px;
  background-color: #D82E3B;
  border-color: #D82E3B;
}

nav .btn:hover {
  background-color: #FFFFFF; /* white */
  color: black;
}
nav label {
  font-size: 20pt;
  color:white;
}


</style>
