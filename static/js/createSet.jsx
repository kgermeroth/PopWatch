// Creates plus sign icon
class Add extends React.Component {
	render() {
		return (
			<p>Add Hotel: <i className="fas fa-plus"></i></p> 
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

// this is the dropdown to select a hotel
class HotelNameSelector extends React.Component {
	constructor() {
		super();		
	}
	
	render() {
		// create an empty list
		const hotel_options = [];

		hotel_options.push(<option key="" defaultValue>Select Hotel</option>)

		// Loop through each hotel in the hotels property (JSON object), and append an option tag with the hotel variables inside
		for (const hotel of this.props.hotels) {
			hotel_options.push(<option  placeholder="Select Hotel" key={hotel.hotel_id} value={hotel.hotel_id}>{hotel.hotel_name}</option>);
		}

		// return the array of options in select tags
		return <select>{hotel_options}</select>
			
	}
}

// Test combining both elements (and see if icons render)
class HotelContainer extends React.Component {
	constructor() {
		super();
		this.state = {
			hotels:[]
		}
	}

	//when this component mounts, change the state to be equal to the get results (MUST have a success function)
	componentDidMount() {
		const hotels = $.get('/hotels.json', (hotels)=> this.setState({
			hotels
		}));

	}
	render() {
		return (<div>
			<HotelNameSelector hotels={this.state.hotels}/>
			<Trash />
			</div>
		);
	}
}

ReactDOM.render(
	<HotelContainer />,
	document.getElementById("hotel-dropdowns")
	);

ReactDOM.render(
	<Add />,
	document.getElementById("add-hotel")
	);

