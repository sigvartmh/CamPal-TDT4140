#include <opencv2/opencv.hpp> //Include file for every supported OpenCV function
using namespace std;

//using namespace cv;
using namespace std;

int main( int argc, char** argv )
{
    cout << "OpenCV version : " << CV_VERSION << endl;
    cout << "Major version : " << CV_MAJOR_VERSION << endl;
    cout << "Minor version : " << CV_MINOR_VERSION << endl;
    cout << "Subminor version : " << CV_SUBMINOR_VERSION << endl;
    cv::VideoCapture cap; // open the default camera
    cap.open(0);
    cv::namedWindow( "Example1", cv::WINDOW_AUTOSIZE );
    cv::Mat frame;
    for(;;){
    cap.read(frame);
    cv::imshow( "Example1", frame );
    cv::waitKey(33);
    }
    cv::waitKey( 0 );
  cv::destroyWindow( "Example1" );
  return 0;
}
