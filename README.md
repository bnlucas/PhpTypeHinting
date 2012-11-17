PHP Type Hinting
================

I prefer the AS3 way of type hiting method parameters **param:Type** where as PHP
offers very limited type hinting; object, array, or class name. This is a Sublime Text
plugin to convert an abstract PHP syntax into type hinted methods. It uses my PHP
utility package, [TypeCheck](https://github.com/bnlucas/Utilities/blob/master/TypeCheck.php) for parameter type checking.

Abstract method syntax:
=======================
```php
use Utilities\TypeCheck as TypeCheck;

class ErrorHandler {

	protected static $application:String;

	public static function register($application:*, $exceptions:bool = true):void;

	public static function unregister():void;

	public static function handleException($exception:Exception):void
}
```

After running PHP Type Hinting
==============================
```php
use Utilities\TypeCheck as TypeCheck;

class ErrorHandler {

	/**
	 * @access protected
	 * @static
	 * @var string $application
	 */
	protected static $application;

	/**
	 * register
	 *
	 * @access public
	 * @static
	 * @param mixed $application
	 * @param bool $exceptions
	 * @return void
	 */
	public static function register($application, $exceptions = true) {
		TypeCheck::check("mixed", "bool");
		
	}

	/**
	 * unregister
	 *
	 * @access public
	 * @static
	 * @return void
	 */
	public static function unregister() {
		
	}

	/**
	 * handleException
	 *
	 * @access public
	 * @static
	 * @param Exception $exception
	 * @return void
	 */
	public static function handleException(Exception $exception) {
		TypeCheck::check("object");
		
	}
}
```

There are three ways of calling the plugin:

1. Tools->PHP->PHP Type Hinting
2. From the context menu, PHP Type Hinting...
3. Keystroke Ctrl+K + Ctrl+T