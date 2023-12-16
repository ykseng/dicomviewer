# style for slicing 
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage


# Helper class to format slice status message
class StatusMessage:
    @staticmethod
    def format(slice: int, max_slice: int):
        return f'Slice: {slice + 1}/{max_slice + 1}'

# this is the class for main python to call the modified vtk interactor style in slicing
# Define own interaction style
class MyVtkInteractorStyleImage(vtkInteractorStyleImage):
    def __init__(self, parent=None):
        super().__init__()
        # add observer
        self.AddObserver('KeyPressEvent', self.KeyPressEvent)
        self.AddObserver('MouseWheelForwardEvent', self.MouseWheelForwardEvent)
        self.AddObserver('MouseWheelBackwardEvent', self.MouseWheelBackwardEvent)
        self.image_viewer = None
        self.status_label = None
        self.slice = 0
        self.min_slice = 0
        self.max_slice = 0

    def set_image_viewer(self, image_viewer):
        # get image viewer from the main class
        self.image_viewer = image_viewer
        self.min_slice = image_viewer.GetSliceMin()
        self.max_slice = image_viewer.GetSliceMax()
        self.slice = int((self.min_slice+self.max_slice)/2)
        self.image_viewer.SetSlice(self.slice)
        #print(f'Slicer: Min = {self.min_slice}, Max= {self.max_slice}')

    def set_status_label(self, status_label):
        # show slicing number  label in main window
        self.status_label = status_label
        msg = StatusMessage.format(self.slice, self.max_slice)
        self.status_label.setText(msg)


    def set_status_bar(self, bar1, bar2):
        # for the bar get from main
        self.bar1=bar1
        self.bar2=bar2
        bar1.setMaximum(self.max_slice)
        bar2.setMaximum(self.max_slice)
        bar1.setValue(self.slice)
        bar2.setValue(self.slice)
        # detect the slice and change it
        bar1.valueChanged.connect(self.slider_changed)
        bar2.valueChanged.connect(self.slider_changed)

    def slider_changed(self, value):
        # change the slice when move the bar
        self.image_viewer.SetSlice(value)

        msg = StatusMessage.format(value, self.max_slice)
        self.status_label.setText(msg)
        self.slice=value
        self.bar1.setValue(self.slice)
        self.bar2.setValue(self.slice)

    def move_slice_forward(self):
        if self.slice < self.max_slice:
            self.slice += 1
            #print(f'MoveSliceForward::Slice = {self.slice}')
            self.image_viewer.SetSlice(self.slice)
            msg = StatusMessage.format(self.slice, self.max_slice)
            self.status_label.setText(msg)
            self.bar1.setValue(self.slice)
            self.bar2.setValue(self.slice)

    def move_slice_backward(self):
        if self.slice > self.min_slice:
            self.slice -= 1
            #print(f'MoveSliceBackward::Slice = {self.slice}')
            self.image_viewer.SetSlice(self.slice)
            msg = StatusMessage.format(self.slice, self.max_slice)
            self.status_label.setText(msg)
            self.bar1.setValue(self.slice)
            self.bar2.setValue(self.slice)

    def KeyPressEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key == 'Up':
            self.move_slice_forward()
        elif key == 'Down':
            self.move_slice_backward()

    def MouseWheelForwardEvent(self, obj, event):
        self.move_slice_forward()
        

    def MouseWheelBackwardEvent(self, obj, event):
        self.move_slice_backward()
        
