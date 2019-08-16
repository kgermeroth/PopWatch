// This component is the add sign
class Add extends React.Component {
	constructor() {
		super();
		this.addHotel = this.addHotel.bind(this);
	}

	// This function will create a new HotelContainer, but is executed in HotelDropDowns
	addHotel() {
		this.props.onClick()
	}

	render() {
		return (
			<p>Add Hotel: <i onClick={this.addHotel} className="fas fa-plus"></i></p> 
			);
	}
}

// This component is the trash icon
class Trash extends React.Component {
	constructor() {
		super();
	}

	render() {
		return (
			<i onClick={this.props.handleOnClick} className="fas fa-trash"></i>
			);
	}
}

// this is the dropdown to select a hotel
class HotelNameSelector extends React.Component {
	constructor() {
		super();		 
	}

	// handleChange(event) {
	// 	this.props.handleOnClick(event.target.value);
	// }
	
	render() {
		// create an empty list
		const hotel_options = [];

		//adds the default "Select Hotel" to the hotel_options list
		hotel_options.push(<option key="0" defaultValue>Select Hotel</option>)

		// Loop through each hotel in the hotels property (JSON object), and append an option tag with the hotel variables inside
		// the list of hotels comes from the property on the HotelContainer class which comes from the state on the HotelDropDowns when the component mounts
		for (const hotel of this.props.hotels) {
			hotel_options.push(<option key={hotel.hotel_id} value={hotel.hotel_id}>{hotel.hotel_name}</option>);
		}

		// return the array of options in select tags
		// return <select name="hotel_choice[]" onChange={this.handleChange}>{hotel_options}</select>
		return <select name="hotel_choice[]">{hotel_options}</select>
			
	}
}

// This component holds the HotelNameSelector (hotel dropdown) and the trash icon
class SingleHotelContainer extends React.Component {
	constructor() {
		super();
	}
	// write handleChange function with event to get hotel_id

	// render() {
	// 	return (<div className="HotelContainer">
	// 		<HotelNameSelector hotels={this.props.hotels} handleChange={this.props.handleChange}/>
	// 		<Trash handleOnClick={this.props.handleDropContainer} />
	// 		</div>
	// 	);
	// }

	render() {
		return (<div className="HotelContainer">
			<HotelNameSelector hotels={this.props.hotels} />
			<Trash handleOnClick={this.props.handleDropContainer} />
			</div>
		);
	}
}

// This component holds everything: multiple HotelContainers (which are the hotel dropdown and trash icon) and the addHotel icon
class HotelDropDowns extends React.Component {

    constructor() {
    	super();
        this.state = {
            hotels: [],
            hotelContainers: [
            	{hotel_id: 0}			
            ]
        };
        this.addHotel = this.addHotel.bind(this);
        this.dropHotelContainer = this.dropHotelContainer.bind(this);
        // this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
	// AJAX request to get a list of hotels from db
		const hotels = $.get('/hotels.json', (hotels)=> this.setState({
			hotels
		}));
    }

    // handleChange(value, idx) {
    // 	const hotelContainers = this.state.hotelContainers;

    // 	const selected_hotel = event.target.value;

    // 	hotelContainers[idx] = {"hotel_id": value};

    // 	this.setState({hotelContainers});
    // }

    addHotel() {
    	
    	const hotelContainers = this.state.hotelContainers;

    	// add a new hotel container to the list (not a JSX, just data)
    	hotelContainers.push({"hotel_id": 0});

    	// update the react state
    	this.setState({hotelContainers});

    }

    dropHotelContainer(idx) {
    	// const hotelContainers = this.state.hotelContainers.filter((container, i) =>{
    	// 	return i !== idx;
    	// });

    	const hotelContainers = this.state.hotelContainers;
		hotelContainers.splice(idx, 1);
		const newhotelContainers = hotelContainers

    	this.setState({hotelContainers: newhotelContainers});
    }

    render() {

        const hotelContainers = []

        // this.state.hotelContainers.map((hotelContainer, idx) => {
        //         hotelContainers.push(
        //         	<SingleHotelContainer
        //         	key={idx}
        //         	handleDropContainer={() => this.dropHotelContainer(idx)}
        //         	handleChange={this.handleChange({idx})}
        //         	hotels={this.state.hotels}
        //         />
        //         )

        this.state.hotelContainers.map((hotelContainer, idx) => {
                hotelContainers.push(
                	<SingleHotelContainer
                	key={idx}
                	handleDropContainer={() => this.dropHotelContainer(idx)}
                	hotels={this.state.hotels}
                />
                )
        });

        return (
            <div>
                <div className="selected-hotels">
                    {hotelContainers}
                </div>

                <Add onClick={this.addHotel}/>
           </div> 
        );
	};
}

ReactDOM.render(
	<HotelDropDowns />,
	document.getElementById("hotel-dropdowns")
	);