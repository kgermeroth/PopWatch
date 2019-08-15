// Creates plus sign icon
class Add extends React.Component {
	render() {
		return (
			<i className="fas fa-plus"></i> 
			);
	}
}

// Creates trashcan icon
class Trash extends React.Component {
	render() {
		return (
			<i className="fas fa-trash"></i>
			);
	}
}


// Test combining both elements (and see if icons render)
class Test extends React.Component {
	render() {
		return (
			React.createElement('div', null,
			React.createElement(Trash, null,),
			React.createElement(Add, null)
			));
	}
}

ReactDOM.render(
	React.createElement(Test, null),
	document.getElementById("root")
	);

