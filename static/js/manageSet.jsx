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
			<p><b>Add Hotel: </b><i 
			onClick={this.addHotel} 
			className="fas fa-plus"
			></i></p> 
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
	
	render() {
		// create an empty list
		const hotel_options = [];

		//adds the default "Select Hotel" to the hotel_options list
		hotel_options.push(<option key="0" defaultValue>Select Hotel</option>)

		// Loop through each hotel in the hotels property (JSON object), and append an option tag with the hotel variables inside
		// the list of hotels comes from the property on the HotelContainer class which comes from the state on the HotelDropDowns when the component mounts
		for (const hotel of this.props.hotels) {
			// See if hotel is in the selected hotels list. If it's not then add to the dropdowns.
			// Also checks to see if the value matches the hotel id, will display the name for the dropdown it is
			// selected for, but not the others (because the value is specific to dropdown on which it was selected)
			if ((!(this.props.selectedHotels.includes(hotel.hotel_id))) || this.props.value === hotel.hotel_id) {
				hotel_options.push(<option key={hotel.hotel_id} value={hotel.hotel_id}>{hotel.hotel_name}</option>);
			}
		}

		// return the array of options in select tags
		// ternary can be used for disabled, what is below is shorthand for that (if condition is true, returns thing to the left of colon, if false returns things to the right)
		return (
			<select
				className="hotel_dropdown"
				name="hotel_choice[]"	
				onChange={this.props.handleChange}
				value={this.props.value}
				disabled={this.props.value > 0}
			>
				{hotel_options}
			</select>
		);
			
	}
}

// This component holds the HotelNameSelector (hotel dropdown) and the trash icon
class SingleHotelContainer extends React.Component {
	constructor() {
		super();
	}

	render() {
		return (<div className="HotelContainer">
			<HotelNameSelector
				hotels={this.props.hotels}
				handleChange={this.props.handleChange}
				value={this.props.selectedHotel}
				selectedHotels={this.props.selectedHotels}
			/>
			<Trash handleOnClick={this.props.handleDropContainer} />
			</div>
		);
	}
}

// This component is the dropdown that lists all the comp sets
class CompSetDropdown extends React.Component {
	constructor () {
		super();
	}

	render() {

		const comp_sets = [];

		for (const set of this.props.compSetNames) {
			comp_sets.push(<option key={set.view_id} value={set.view_id} selected={this.props.currentSetChoice === set.view_id}>{set.view_name}</option>);
		}

		return (
			<select
				className="comp_set_dropdown"
				name="comp_sets"
				onChange={this.props.onChange}
				>{ comp_sets }</select>)
	}
}

// This component holds everything: multiple HotelContainers (which are the hotel dropdown and trash icon) and the addHotel icon
class AllHotelDropDowns extends React.Component {

    constructor() {
    	super();
        this.state = {
            hotels: [],
            defaultView: null,
            compSetNames: [],
            compSetHotels: [],
            hotelContainers: [],
            selectedHotels: [],
            currentSetChoice: null
        };
        this.addHotel = this.addHotel.bind(this);
        this.dropHotelContainer = this.dropHotelContainer.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
	// AJAX request to get a list of hotels from db
		const hotels = $.get('/sets.json', (data)=> {

			const defaultHotelsSelected = data['hotels_in_views'][data['default_view']];
			const newHotelContainers = this.state.hotelContainers.slice();
			const newSelectedHotels = this.state.selectedHotels;
			
			for (const hotel of defaultHotelsSelected) {
				newHotelContainers.push({ selectedHotel: hotel });
				newSelectedHotels.push(hotel);
			}

			this.setState({ hotels: data['hotels'],
							defaultView: data['default_view'],
							compSetNames: data['view_names'],
							compSetHotels: data['hotels_in_views'],
							hotelContainers: newHotelContainers,
							selectedHotels: newSelectedHotels,
							currentSetChoice: data['default_view']
						})
		})
    }

    handleChange(idx, event) {
    	const newHotelContainers = this.state.hotelContainers.slice();
    	const newSelectedHotels = this.state.selectedHotels.slice();
    	const value = parseInt(event.target.value,10);

    	newHotelContainers[idx] = { selectedHotel: value };
    	newSelectedHotels.push(value);

    	this.setState({ hotelContainers: newHotelContainers,
    					selectedHotels: newSelectedHotels });    	
    }

    addHotel() {
    	
    	const hotelContainers = this.state.hotelContainers;

    	if (hotelContainers.length < 8) {
	    	// add a new hotel container to the list, this will create a new hotel container
	    	hotelContainers.push({ selectedHotel: 'Select Hotel' });
	    	 // update the react state
    		this.setState({ hotelContainers });
	    } else {
	    	alert('There is a maximum of 8 hotels.');
	    }
    }

    dropHotelContainer(idx, selectedHotel) {
    	console.log('selected hotel was: ', selectedHotel)

    	const newSelectedHotels = this.state.selectedHotels.slice();

    	// loop through selected hotels and remove the hotel that was just removed
    	newSelectedHotels.map((selection, idx) => {
    		if (selection === selectedHotel) {
    			newSelectedHotels.splice(idx,1)
    		}
    	});

    	// make a copy of newHotelContainers and splice the appropriate hotelContainer
    	const newHotelContainers = this.state.hotelContainers.slice();
		newHotelContainers.splice(idx, 1);
		

    	this.setState({hotelContainers: newHotelContainers,
    					selectedHotels: newSelectedHotels });
    }

    changeCompSet(event) {
    	// update selected hotel
    	const newSetChoice = parseInt(event.target.value,10);
    	const newHotelContainers = [];
    	const newSelectedHotels = [];

    	// update hotelContainers
    	for (const hotel of this.state.compSetHotels[newSetChoice]) {
			newHotelContainers.push({ selectedHotel: hotel });
			newSelectedHotels.push(hotel);
		}

		this.setState({	currentSetChoice: newSetChoice,
						hotelContainers: newHotelContainers,
						selectedHotels: newSelectedHotels
		})

    }

    render() {

        const hotelContainers = this.state.hotelContainers.map((hotelContainer, idx) => {
            return (
            	<SingleHotelContainer
                	key={idx}
                	handleDropContainer={() => this.dropHotelContainer(idx, hotelContainer.selectedHotel)}
                	handleChange={(event) => this.handleChange(idx, event)} 
                	hotels={this.state.hotels}
                	selectedHotel={hotelContainer.selectedHotel}
                	selectedHotels={this.state.selectedHotels}
                	
            	/>
            );
        });

        return (
            <div>
            	<CompSetDropdown 
            		compSetNames={this.state.compSetNames} 
            		currentSetChoice={this.state.currentSetChoice}
            		onChange={(event) => this.changeCompSet(event)}
            	/>
                <div className="selected-hotels">
                    {hotelContainers}
                </div>

                <Add onClick={this.addHotel}/>
           </div> 
        );
	};
}

ReactDOM.render(
	<AllHotelDropDowns />,
	document.getElementById("manage_set")
	);