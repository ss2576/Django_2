   def __init__(self, *args, **kwargs):
       super(OrderItemForm, self).__init__(*args, **kwargs)
       for field_name, field in self.fields.items():
           field.widget.attrs['class'] = 'form-control'
	   self.fields['product'].queryset = Product.get_items()