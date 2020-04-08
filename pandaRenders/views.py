from rest_pandas import PandasView, PandasSimpleView
from api.models import IndAgency, Bank
from api.serializers import BankSerializer
import pandas as pd


# Short version (leverages default DRP settings):
def transform_dataframe(dataframe):
    dataframe.some_pivot_function(in_place=True)
    return dataframe


class IndAgencyView(PandasView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    # That's it!  The view will be able to export the model dataset to any of
    # the included formats listed above.  No further customization is needed to
    # leverage the defaults.

    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            # Use custom filename and Content-Disposition header
            return "Data Export"  # Extension will be appended automatically
        else:
            # Default filename from URL (no Content-Disposition header)
            return None



# class BankView(PandasView):
#     queryset = Bank.objects.all()
#     frame = pd.read_frame(queryset)
#     serializer_class = BankSerializer
#
#
# class IndView(PandasSimpleView):
#     def get_data(self, request, *args, **kwargs):
#         queryset = Bank.objects.all()
#         frame = pd.read_frame(queryset)
#         return frame

# # Long Version and step-by-step explanation
# class TimeSeriesView(PandasView):
#     # Assign a default model queryset to the view
#     queryset = TimeSeries.objects.all()
#
#     # Step 1. In response to get(), the underlying Django REST Framework view
#     # will load the queryset and then pass it to the following function.
#     def filter_queryset(self, qs):
#         # At this point, you can filter queryset based on self.request or other
#         # settings (useful for limiting memory usage).  This function can be
#         # omitted if you are using a filter backend or do not need filtering.
#         return qs
#
#     # Step 2. A Django REST Framework serializer class should serialize each
#     # row in the queryset into a simple dict format.  A simple ModelSerializer
#     # should be sufficient for most cases.
#     serializer_class = TimeSeriesSerializer  # extends ModelSerializer
#
#     # Step 3.  The included PandasSerializer will load all of the row dicts
#     # into array and convert the array into a pandas DataFrame.  The DataFrame
#     # is essentially an intermediate format between Step 2 (dict) and Step 4
#     # (output format).  The default DataFrame simply maps each model field to a
#     # column heading, and will be sufficient in many cases.  If you do not need
#     # to transform the dataframe, you can skip to step 4.
#
#     # If you would like to transform the dataframe (e.g. to pivot or add
#     # columns), you can do so in one of two ways:
#
#     # A. Create a subclass of PandasSerializer, define a function called
#     # transform_dataframe(self, dataframe) on the subclass, and assign it to
#     # pandas_serializer_class on the view.  You can also use one of the three
#     # provided pivoting serializers (see Advanced Usage below).
#     #
#     # class MyCustomPandasSerializer(PandasSerializer):
#     #     def transform_dataframe(self, dataframe):
#     #         dataframe.some_pivot_function(in_place=True)
#     #         return dataframe
#     #
#     pandas_serializer_class = MyCustomPandasSerializer
#
#     # B. Alternatively, you can create a custom transform_dataframe function
#     # directly on the view.  Again, if no custom transformations are needed,
#     # this function does not need to be defined.
#     def transform_dataframe(self, dataframe):
#         dataframe.some_pivot_function(in_place=True)
#         return dataframe
#
#     # NOTE: As the name implies, the primary purpose of transform_dataframe()
#     # is to apply a transformation to an existing dataframe.  In PandasView,
#     # this dataframe is created by serializing data queried from a Django
#     # model.  If you would like to supply your own custom DataFrame from the
#     # start (without using a Django model), you can do so with PandasSimpleView
#     # as shown in the first example.
#
#     # Step 4. Finally, the provided renderer classes will convert the DataFrame
#     # to any of the supported output formats (see above).  By default, all of
#     # the formats above are enabled.  To restrict output to only the formats
#     # you are interested in, you can define renderer_classes on the view:
#     renderer_classes = [PandasCSVRenderer, PandasExcelRenderer]
#
#     # You can also set the default renderers for all of your pandas views by
#     # defining the PANDAS_RENDERERS in your settings.py.
#
#     # Step 5 (Optional).  The default filename may not be particularly useful
#     # for your users.  To override, define get_pandas_filename() on your view.
#     # If a filename is returned, rest_pandas will include the following header:
#     # 'Content-Disposition: attachment; filename="Data Export.xlsx"'
#     def get_pandas_filename(self, request, format):
#         if format in ('xls', 'xlsx'):
#             # Use custom filename and Content-Disposition header
#             return "Data Export"  # Extension will be appended automatically
#         else:
#             # Default filename from URL (no Content-Disposition header)
#             return None
